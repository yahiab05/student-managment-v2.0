from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import QDate, QPropertyAnimation, QEasingCurve
from app.repo.database import SessionLocal
from ..repo.models import Students
from ..models.person import Student
from sqlalchemy.exc import IntegrityError
from ..view.students_tables import StudentsSearchTableModel, StudentsTableModel, StudentsHistoryTableModel
from os import path
from ..repo.schemas import SchemaFactory
from ..utils.combo_manager import ComboManager
from ..utils.utils import error, get_username


class StudentsLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        ui_path = path.abspath("./ui/students.ui")
        loadUi(ui_path, self)

        self.identifier = None
        self.model = None
        
        session = SessionLocal()
        self.manager = Student(session)
        self.combo_manager = ComboManager(session)

        self.to.setDate(QDate.currentDate())
        self.date_inscrit.setDate(QDate.currentDate())
        self.gender_search.setCurrentIndex(-1)

        self.animation = QPropertyAnimation(self.search_frame, b"maximumWidth")
        self.animation.setDuration(500)  # 500ms animation
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.search_section("minimize")

        self.setup_table()

        self.setup_ui()

    def setup_ui(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.controls("add"))
        self.update_btn.clicked.connect(lambda: self.controls("update"))
        self.delete_btn.clicked.connect(self.security)
        self.minimize.clicked.connect(lambda: self.search_section("minimize"))
        self.maximize.clicked.connect(lambda: self.search_section("maximize"))
        self.reset_btn.clicked.connect(self.reset_filters)
        self.student_tab.doubleClicked.connect(self.select_student)
        self.search_btn.clicked.connect(self.show_table)
        self.new_year.clicked.connect(self.set_new_year)
        self.printing_btn.clicked.connect(self.export("print"))
        self.export_btn.clicked.connect(self.export("excel"))

    def setup_table(self):
        session = SessionLocal()

        self.model = StudentsTableModel(session)

        self.student_tab.setModel(self.model)

        session.close()

    def controls(self, action):
        name = self.name.text()
        parent = self.parent.text()
        num_tel = self.num_tel.text()
        num_tel_2 = self.num_tel_2.text()
        cin = self.cin.text()
        activity = self.activity.currentText()
        excused = self.excused.currentText()
        date = self.date_inscrit.date()

        if action == "add":
            if self.manager.exists(name, parent):
                error("التلميذ موجود")
                return
        else:
            if self.identifier is None:
                error("يرجى تحديد التلميذ")
                return

        entity = SchemaFactory.STUDENT.create(
            name=name,
            birthday=self.birthday.date().toPyDate(),
            date_inscrit=date.toPyDate(),
            note=self.note.text(),
            user=get_username(),
            gender=self.gender.currentText(),
            parent=parent,
            cin=cin,
            activity=activity,
            num_tel=f"{num_tel}/{num_tel_2}" if num_tel_2 else num_tel,
            excused=excused, 
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
                student_id = self.manager.get_last_student().num_inscrit
                self.add_ensurance(student_id, "تأمين")
                self.add_history(student_id, date)
            except Exception as e:
                error(str(e))
                self.manager.db.rollback()
                return
        else:
            try:
                self.manager.update(id=self.identifier, data_obj=entity)
                self.identifier = None
            except Exception as e:
                error(str(e))
                self.manager.db.rollback()
                return

        self.reset()
        self.show_table()
    
    def add_ensurance(self, student_id, class_name):
        ensurance = SchemaFactory.ENROLLMENT.create(
            student_id=student_id, 
            class_name=class_name
            )
        try:
            if not ensurance.validate():
                error("الرجاء ملء جميع الحقول")
                return
        except ValueError as e:
            error(str(e))
            return  
        
        try:
            self.manager.enrollments.create(ensurance)
        except IntegrityError as e:
            self.manager.db.rollback()
            error(str(e))
            return
        
    def select_student(self):
        row = self.student_tab.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()
        
        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)
        self.student_tab.clearSelection()
        self.repopulate()

    def repopulate(self):
        student = self.manager.get_by_id(self.identifier)

        if student is not None:	
            self.name.setText(student.name)
            self.birthday.setDate(student.get_birthday())
            self.parent.setText(student.parent)
            self.cin.setText(str(student.cin))
            self.activity.setCurrentText(student.activity)
            self.excused.setCurrentText(student.excused)
            self.date_inscrit.setDate(student.get_date_inscrit())
            self.gender.setCurrentText(student.gender)
            self.note.setText(student.note)
            nums = student.num_tel.split("/")
            self.num_tel.setText(nums[0])
            if len(nums) == 2:
                self.num_tel_2.setText(nums[1])

    def security(self):
        msg = QMessageBox()
        text = "متأكد من حذف هذا التلميذ ؟"
        btn = 'حذف'

        ret = msg.question(self, btn, text, msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.manager.delete(self.identifier)

        self.reset()
        self.identifier = None
        self.show_table()

    def search_section(self, action):
        if action == "minimize":
            self.animation.setStartValue(200)
            self.animation.setEndValue(0)
        elif action == "maximize":
            self.animation.setStartValue(0)
            self.animation.setEndValue(200)
        else:
            print("not recognized")
        
        self.animation.start()

    def set_new_year(self):
        student = self.manager.get_by_id(self.identifier)
        if student is not None:
            try:
                student.date_inscrit = student.set_date_inscrit(QDate.currentDate())
                self.manager.db.commit()
                self.add_history(self.identifier, QDate.currentDate())
            except Exception:
                self.manager.db.rollback()
                error("هذا التلميذ موجود.")

        else:	
            error("هذا التلميذ غير موجود.")

        self.identifier = None
        self.show_table()
    
    def add_history(self, student_id, date): 
        entity = SchemaFactory.STUDENT_HISTORY.create(
            student_id=student_id,
            date_inscrit= self.manager.history.set_date(date),
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
            self.manager.history.create(entity)
        except IntegrityError as e:
            self.manager.db.rollback()
            error("لم تتم الاضافة")


    def reset(self):
        self.name.setText("")
        self.birthday.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        self.parent.setText("")
        self.num_tel.setText("")
        self.num_tel_2.setText("")
        self.cin.setText("")
        self.activity.setCurrentText("")
        self.excused.setCurrentText("")
        self.date_inscrit.setDate(QDate.currentDate())

    def reset_filters(self):
        self.search_by_name.setText("")
        self.du.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        self.to.setDate(QDate.currentDate())
        self.excused_search.setCurrentIndex(0)
        self.activity_search.setCurrentIndex(0)
        self.gender_search.setCurrentIndex(-1)

    def show_table(self):
        du = self.du.date()
        au = self.to.date()
        
        excused = self.excused_search.currentText()
        if excused == "":
            excused = None
            
        activity = self.activity_search.currentText()
        
        gender = self.gender_search.currentText()
        if gender == "":
            gender = None
        
        name = self.search_by_name.text()
        if name == "":
            name = None

        filters = self.manager.get_filters(
            name=name,
            gender=gender,
            _from=du,
            _to=au,
            excused=excused,
            activity=activity
        )
        data = self.manager.get_by_filter(filters)

        self.model.refresh(data)
        self.nb.setText(str(self.model.rowCount()))
        
    def export(self, output_channel: str):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(
            data_to_export=data_to_export, 
            row_count=row_count
            )
        
        if output_channel == "print":
            self.print_preview()
        elif output_channel == "excel":
            self.excel()
        else:
            ValueError(f"Unknown output channel: {output_channel}")

    def print_preview(self):
        try:
            self.manager.print_preview(self)
        except ValueError as e:
            error("لا يمكنك الطباعة")
        except Exception as e:
            error("لا يمكنك الطباعة")

    def excel(self):
        try:
            self.manager.export_to_excel(self)
        except Exception as e:
            error("لا يمكنك تحميل الملف")


class StudentsHistoryLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = path.abspath("./ui/student_history.ui")
        loadUi(ui_path, self)

        self.model = None

        self.setup_table()

        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(lambda: self.num_ins_search.setText(""))
        self.printing_btn.clicked.connect(self.print_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = StudentsHistoryTableModel(session)

        self.student_tab.setModel(self.model)

    def search(self):
        identifier = self.num_ins_search.text()
        
        if identifier == "":
            identifier = None

        self.model.refresh(identifier)

    def print_preview(self):
        try:
            title = "قائمة التلميذ"

            intro = self.model.intro

            header = ["معفى", "رقم الهاتف", 'سنوات الدراسة', "تاريخ الولادة", "الإسم"]

            foot = "المجموع: " + str(self.model.rowCount())

            data = []

            for student in self.model.students:
                row = [
                    student.student.excused,
                    student.student.num_tel,
                    student.date_inscrit.strftime("%Y-%m-%d"),
                    student.student.birthday.strftime("%Y-%m-%d"),
                    student.student.name
                ]
                data.append(row)
            
            printer = Printing()
            printer.setup_document(data, header, title, intro, foot)
            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")


    def excel(self):
        try:
            header = ["معفى", "رقم الهاتف", 'سنوات الدراسة', "تاريخ الولادة", "الإسم"]
            data = []

            for student in self.model.students:
                row = [
                    student.student.excused,
                    student.student.num_tel,
                    student.date_inscrit.strftime("%Y-%m-%d"),
                    student.student.birthday.strftime("%Y-%m-%d"),
                    student.student.name
                ]
                data.append(row)

            HelpLogic.excel(self, header, data)

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

class ClassesPerStudentLogic(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        ui_path = path.abspath("./ui/classes_per_student.ui")
        loadUi(ui_path, self)

        self.model = None
        self.name = ""

        self.setup_table()
        self.setup()

    def setup(self):
        self.reset_btn.clicked.connect(self.reset)
        self.search_ent.textChanged.connect(self.student_search)
        self.student_list.doubleClicked.connect(self.list_of_classes)

    def setup_table(self):
        session = SessionLocal()

        self.model = StudentsSearchTableModel(session)

        self.student_list.setModel(self.model)

        session.close()

    def student_search(self):
        name = self.search_ent.text()

        self.model.refresh(name)
        self.student_list.repaint()

    def get_id(self):
        row = self.student_list.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()

        self.name = self.model.data(self.model.index(row_index, 1), role=0)	

        return self.model.data(self.model.index(row_index, 0), role=0)

    def list_of_classes(self):
        id = self.get_id()

        session = SessionLocal()

        classes = session.query(ClassEleve).with_entities(ClassEleve.class_name).filter(ClassEleve.student_id == id, ClassEleve.class_name != "تأمين").all()

        session.close()

        self.class_list.clear()

        if classes:
            for class_name in classes:
                self.class_list.addItem(class_name[0])

        else:
            HelpLogic.error("لا يوجد صفوف لهذا التلميذ")


    def reset(self):
        self.search_ent.setText("")
        self.class_list.clear()

if __name__ == '__main__':
    app = QApplication([])
    window = Students()
    window.show()
    app.exec()
