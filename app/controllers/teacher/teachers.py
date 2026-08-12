from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate
from os import path
from sqlalchemy.exc import IntegrityError
from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.repo.schemas import SchemaFactory
from app.utils import error, get_username, get_combo_manager, ReportType, WorkingMode
from app.ui.ui_forms import TeacherUI, TeacherHistoryUI
from app.controllers.popup import create_popup_factory, PopupKind


class TeacherLogic(QWidget, TeacherUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = path.abspath(path.join(path.dirname(__file__), "..", "ui", "teacher", "teacher.ui"))

        loadUi(ui_path, self)

        self.model = None
        self.manager = get_model(ModelName.TEACHERS)
        self.combo_manager = get_combo_manager()
        self.classes_manager = get_model(ModelName.CLASSES)
        self.history_manager = get_model(ModelName.TEACHERS_HISTORY)

        self.identifier = None
        
        self.setup()
        self.setup_table()
        self.show_teachers()

    def setup(self):
        self.add_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete)
        self.teachers_table.doubleClicked.connect(self.select_row)
        self.search.textChanged.connect(self.show_teachers)
        self.new_year_btn.clicked.connect(self.new_year_security)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.TEACHERS)

        self.teachers_table.setModel(self.model)
        self.teachers_table.hideColumn(self.model.ID_COLUMN)

    def aquire_data(self, action: WorkingMode):
        dialog = create_popup_factory(
            kind=PopupKind.TEACHER, 
            title="إضافة معلم" if action == WorkingMode.ADD else "تعديل معلم", 
            parent=self
        )
        
        if action == WorkingMode.UPDATE:
            if self.identifier is None:
                error("يرجى تحديد معلم")
                return
            data = self.manager.get_by_id(self.identifier)
            dialog.content.repopulate_fields(data.__dict__)
        
        def on_confirm():
            data = dialog.content.get_data()
            self.control(action, data)
            
        dialog.confirmed.connect(on_confirm)
        dialog.show()

    def control(self, action: WorkingMode, data: dict):
        phone1 = data["phone"]
        phone2 = data["phone_2"]

        
        if len(phone2) == 8 and phone2.isdigit():
            phone1 += f"/{phone2}"
            
        
        entity = SchemaFactory.TEACHER(
            name=data["name"],
            date_inscrit=data["date_inscrit"],
            birthday=data["birthday"],
            phone=phone1,
            note=data["note"],
            user=get_username()
        )
        
        try:
            if not entity.validate():
                error("الرجاء ملء جميع الحقول")
                return
        except ValueError as e:
            error(str(e))
            return
    
        if action == WorkingMode.ADD:
            try: 
                self.manager.create(entity)
                self.add_history(self.manager.get_last_id(), 
                                date_inscrit=data["date_inscrit"] 
                                )                
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
        self.combo_manager.update_cache_from_db("teachers")

    def delete(self):
        if self.identifier is not None and not self.has_classes():
            line = self.manager.get_by_id(self.identifier)
            name = line[0].name
            try:
                if not self.has_classes():
                    self.manager.delete(self.identifier)
                    self.identifier = None  # Reset identifier after deletion
                    self.show_teachers()
                    self.combo_manager.update_cache_from_db("teachers")
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
                teacher[0].date_inscrit = teacher.set_date_iscrit(QDate.currentDate())
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
            
    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(data_to_export, row_count)
        
        self.manager.export_data(
            report_type=output_channel, 
            parent=self
            )

class TeachersHistoryLogic(QWidget, TeacherHistoryUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = path.abspath(path.join(path.dirname(__file__), "..", "ui", "teacher", "teacher_history.ui"))
        loadUi(ui_path, self)

        self.model = None
        self.manager = get_model(ModelName.TEACHERS_HISTORY)
        
        self.setup_table()
        self.setup()


    def setup(self):
        self.search_btn.clicked.connect(lambda: self.show_table(self.search.text()))
        self.reset_btn.clicked.connect(lambda: self.search.setText(""))
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.TEACHER_HISTORY)

        self.history_table.setModel(self.model)
        self.history_table.hideColumn(self.model.ID_COLUMN)

    def show_table(self, teacher_id=None):
        if teacher_id == "": 
            teacher_id = None
        
        data = self.manager.search_by_id(teacher_id)
        
        self.model.refresh(data)    

        self.nb.setText(str(self.model.rowCount()))
        
    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(data_to_export, row_count)
        
        self.manager.export_data(
            report_type=output_channel, 
            parent=self
            )

    
