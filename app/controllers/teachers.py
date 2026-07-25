from wsgiref import headers

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate
from .database import SessionLocal
from os import path
from sqlalchemy.exc import IntegrityError
from ..view.teachers_tables import TeachersTableModel, TeachersHistoryTableModel
from ..models import get_model
from ..utils.combo_manager import ComboManager
from ..repo.schemas import SchemaFactory
from ..utils.utils import error, get_username


class TeacherLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = path.abspath("./ui/teacher.ui")  # Convert to absolute path

        loadUi(ui_path, self)

        self.model = None
        session = SessionLocal()
        self.manager = get_model(session, "teachers")
        self.combo_manager = ComboManager("teachers")
        self.classes_manager = get_model(session, "classes")
        self.history_manager = get_model(session, "teachers_history")

        self.identifier = None
        
        self.setup()
        self.setup_table()
        self.show_teachers()
        self.reset()


    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.delete)
        self.teachers_table.doubleClicked.connect(self.select_row)
        self.search.textChanged.connect(self.show_teachers)
        self.new_year_btn.clicked.connect(self.new_year_security)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = TeachersTableModel(session)

        self.teachers_table.setModel(self.model)

        session.close()

    def control(self, action):
        name = self.name.text()
        date_ins = self.date_inscrit.date()
        birthday = self.birthday.date()
        phone1 = self.phone.text()
        phone2 = self.phone_2.text()
        note = self.note.text()
        money = self.money.currentText()
        
        if len(phone2) == 8 and phone2.isdigit():
            phone1 += f"/{phone2}"
            
        
        entity = SchemaFactory.TEACHER(
            name=name,
            date_inscrit=date_ins,
            birthday=birthday,
            phone=phone1,
            note=note,
            payed=money,
            user=get_username()
        )
        
        try:
            if not entity.validate():
                error("الرجاء ملء جميع الحقول")
                return
        except ValueError as e:
            error(str(e))
            return
    
        if action == "add":
            try: 
                self.manager.create(entity)
                self.add_history(self.manager.get_last_id(), date_ins, money)
            except IntegrityError:
                error("هذا المعلم موجود.")
                return
        else:
            try:
                if self.identifier is None:
                    error("يرجى تحديد معلم")
                    return
                self.manager.update(self.identifier, entity)
                self.identifier = None  # Reset identifier after update
            except IntegrityError as e:
                error("حدث خطأ أثناء تحديث المعلم.")
                return
        self.reset()
        self.show_teachers()

    def delete(self):
        if self.identifier is not None and not self.has_classes():
            line = self.manager.get_by_id(self.identifier)
            name = line.name
            try:
                if not self.has_classes():
                    self.manager.delete(self.identifier)
                    self.identifier = None  # Reset identifier after deletion
                    self.show_teachers()
                else:
                    error(f"لا يمكن حذف المعلم {name} لوجود قسم له")
            except IntegrityError:
                error("حدث خطأ أثناء حذف المعلم.")
                return
        else:	
            error("هذا المعلم غير موجود.")
            
    def has_classes(self, name):
        filters = self.classes_manager.get_filters(exact_teacher=name)
        return self.classes_manager.exists(filters)

    def reset(self):
        self.name.setText("")
        self.date_inscrit.setDate(QDate.currentDate())
        self.birthday.setDate(QDate.currentDate())
        self.phone.setText("")
        self.phone_2.setText("")
        self.note.setText("")

        self.identifier = None

    def select_row(self):
        row = self.teachers_table.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد قسم")
            return
        
        row_index = row[0].row()
        
        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)
        self.repopulate()

    def repopulate(self):
        data = self.manager.get_by_id(self.identifier)
        if data is not None:
            self.name.setText(data.name)
            self.date_inscrit.setDate(data.get_date_inscrit())
            self.birthday.setDate(data.get_birthday())
            if len(data.phone) > 8:
                phones = data.phone.split("/")
                self.phone.setText(phones[0])
                self.phone_2.setText(phones[1])
            else:
                self.phone.setText(data.phone)
            self.note.setText(data.note)
            self.money.setCurrentText(data.payed)

    def show_teachers(self):
        name = self.search.text() 
        
        name = name if name else None

        filters = self.manager.get_filters(name)
        data = self.manager.get_by_filter(filters)
    
        self.model.refresh(data)

        self.nb.setText(str(self.model.rowCount()))

    def new_year_security(self):
        if self.identifier != 0:
            msg = QMessageBox()
            ret = msg.question(None, 'تسجيل', "هل تريد تسجيل هذا المعلم؟", msg.StandardButton.Yes | msg.StandardButton.No)

            if ret == msg.StandardButton.Yes:
                self.add_history(self.identifier, self.date_inscrit.date(), self.money.currentText())
                self.new_year(self.identifier)
        self.reset()
        self.show_teachers()

    def new_year(self, teacher_id):
        teacher = self.manager.get_by_id(teacher_id)
        if teacher is not None:
            try:
                teacher.date_inscrit = teacher.set_date_iscrit(QDate.currentDate())
                self.manager.commit()
            except IntegrityError:
                error("هذا المعلم موجود.")
            finally:
                self.show_teachers()
        else:
            error("هذا المعلم غير موجود.")

    def add_history(self, teacher_id, date, payed):
        entity = SchemaFactory.TEACHER_HISTORY(
            teacher_id=teacher_id,
            date_inscrit=date.toPyDate(),
            payed=payed,
            user=get_username()
        )
        
        try: 
            if not entity.validate():
                error("الرجاء ملء جميع الحقول")
                return
        except ValueError as e:
            error(str(e))
            return
        
        try:
            self.history_manager.create(entity)
        except IntegrityError:
            error("لم تتم الاضافة")
            
    def export(self, output_channel: str):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(data_to_export, row_count)
        
        if output_channel == "excel":
            self.excel()
        elif output_channel == "print":
            self.printing_preview()

    def printing_preview(self):
        try:
            self.manager.print_preview(self)
        except Exception as e:
            print(e)
            error("لا يمكنك الطباعة")

    def excel(self):
        try: 
            self.manager.export_to_excel(self)
        except Exception as e:
            print(e)
            error("لا يمكنك تحميل الملف")


class TeachersHistoryLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = path.abspath("./ui/teacher_history.ui")
        loadUi(ui_path, self)

        self.model = None
        session = SessionLocal()
        self.manager = get_model(session, "teachers_history")
        
        self.setup_tables()
        self.setup()


    def setup(self):
        self.search_btn.clicked.connect(lambda: self.show_table(self.search.text()))
        self.reset_btn.clicked.connect(lambda: self.search.setText(""))
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_tables(self):
        session = SessionLocal()

        self.model = TeachersHistoryTableModel(session)

        self.history_table.setModel(self.model)

        session.close()

    def show_table(self, teacher_id=None):
        if teacher_id == "": teacher_id = None
        if teacher_id is not None:

            self.model.refresh(teacher_id)

        self.nb.setText(str(self.model.rowCount()))

    def printing_preview(self):
        try:

            title = "قائمة الأساتذة"

            headers = ["تاريخ الولادة", "سنوات التدريس", "الإسم", "رقم التسجيل"]

            foot = f"""عدد الأساتذة: {self.model.rowCount()}"""

            data = []

            for teacher in self.model.teachers:
                row = [
                    teacher.teacher.birthday.strftime("%Y-%m-%d"),
                    teacher.date_inscrit.strftime("%Y-%m-%d"),
                    teacher.teacher.name,
                    teacher.teacher_id
                ]
                data.append(row)

            printer = Printing()
            printer.setup_document(data, headers, title, "", foot)

            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        try:
            headers = ["تاريخ الولادة", "سنوات التدريس", "الإسم", "رقم التسجيل"]
            data = []

            for teacher in self.model.teachers:
                row = [
                    teacher.teacher.birthday.strftime("%Y-%m-%d"),
                    teacher.date_inscrit.strftime("%Y-%m-%d"),
                    teacher.teacher.name,
                    teacher.teacher_id
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

    
