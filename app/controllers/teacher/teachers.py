from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate
from sqlalchemy.exc import IntegrityError

from app.utils.combo_names import ComboName
from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.repo.schemas import SchemaFactory
from app.utils import (error, get_username, get_combo_manager, ReportType, WorkingMode, 
                        load_gui, UiPath, traceback_to_string, get_selection_status_stylesheet,
                        set_header_resize_mode)
from app.ui.ui_forms import TeacherUI, TeacherHistoryUI
from app.controllers.popup import create_popup_factory, PopupKind


class TeacherLogic(QWidget, TeacherUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_gui(UiPath.TEACHERS, "teacher.ui", self)

        self.model = None
        self.manager = get_model(ModelName.TEACHERS)
        self.combo_manager = get_combo_manager
        self.classes_manager = get_model(ModelName.CLASSES)
        self.history_manager = get_model(ModelName.TEACHERS_HISTORY)

        self.indentifier = None
        self.deselection()
        
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
        set_header_resize_mode(self.teachers_table, self.model)


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
            dialog.close()
            
        dialog.confirmed.connect(on_confirm)
        dialog.cancel_btn.clicked.connect(lambda: dialog.close())
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
                with self.manager.transaction() as session:
                    self.manager.create(entity, session=session)
                    session.flush()  # Ensure the new teacher is written to the database
                    self.add_history(teacher_id=self.manager.get_last_id(session=session), 
                                    date=data["date_inscrit"],
                                    session=session
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
                self.deselection()
            except IntegrityError as e:
                error("حدث خطأ أثناء تحديث المعلم.")
                return
        self.show_teachers()
        self.combo_manager.update_cache_from_db(ComboName.TEACHER)

    def delete(self):
        if self.identifier is not None:
            line = self.manager.get_by_id(self.identifier)
            name = line.name
            try:
                if not self.has_classes(name):
                    self.manager.sup_security(widget=self, id=self.identifier, text=f"متأكد من حذف المعلم ؟")
                    self.show_teachers()
                    self.deselection()
                    self.combo_manager.update_cache_from_db("teachers")
                else:
                    error(f"لا يمكن حذف المعلم {name} لوجود قسم له")
            except IntegrityError as e:
                print(traceback_to_string(e))
                error("حدث خطأ أثناء حذف المعلم.")
                return
        else:	
            error("هذا المعلم غير موجود.")
            
    def has_classes(self, name):
        filters = self.classes_manager.get_filters(exact_teacher=name)
        return self.classes_manager.exists(filters)

    def select_row(self, index):
        row_index = index.row()
        
        identifier = self.model.data(self.model.index(row_index, 0), role=0)
        self.selection(identifier)
        
    def selection(self, identifier):
        self.identifier = identifier
        self.select_info.setStyleSheet(get_selection_status_stylesheet(True))
        
    def deselection(self):
        self.identifier = None
        self.select_info.setStyleSheet(get_selection_status_stylesheet(False))
        
    def show_teachers(self):
        name = self.search.text() 
        
        name = name if name else None

        filters = self.manager.get_filters(name)
        data = self.manager.get_by_filter(filters)
    
        self.model.refresh(data)

        self.nb.setText(str(self.model.rowCount()))

    def new_year_security(self):
        if self.identifier != 0 and self.identifier is not None:
            msg = QMessageBox()
            ret = msg.question(None, 'تسجيل', "هل تريد تسجيل هذا المعلم؟", msg.StandardButton.Yes | msg.StandardButton.No)

            if ret == msg.StandardButton.Yes:
                with self.manager.transaction() as session:
                    self.add_history(self.identifier, QDate.currentDate().toPyDate(), session=session)
                    self.new_year(self.identifier, session=session)
            
        self.show_teachers()
        self.deselection()

    def new_year(self, teacher_id, session=None):
        teacher = self.manager.get_by_id(teacher_id, session=session)
        if teacher is not None:
            try:
                teacher.date_inscrit = QDate.currentDate().toPyDate()
            except IntegrityError:
                error("هذا المعلم موجود.")
        else:
            error("هذا المعلم غير موجود.")

    def add_history(self, teacher_id, date, session=None):
        entity = SchemaFactory.TEACHER_HISTORY(
            teacher_id=teacher_id,
            date_inscrit=date,
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
            self.history_manager.create(entity, session=session)
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

        load_gui(UiPath.TEACHERS, "teacher_history.ui", self)

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

    
