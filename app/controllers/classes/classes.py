from PyQt6.QtWidgets import QWidget, QApplication
from sqlalchemy.exc import IntegrityError

from app.controllers.popup import create_popup_factory, PopupKind

from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.repo.schemas import SchemaFactory
from app.utils import (
    get_username,
    get_student_list,
    error,
    ReportType,
    get_combo_manager,
    WorkingMode,
    ComboName,
    load_gui,
    UiPath,
    get_selection_status_stylesheet,
    set_header_resize_mode
)
from app.ui.ui_forms import ClassesUI, ClasseleveUI

class ClassesLogic(QWidget, ClassesUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        load_gui(UiPath.CLASSES, "classes.ui", self)

        self.model = None

        self.identifier = 0
        
        self.manager = get_model(ModelName.CLASSES)
        self.combo_manager = get_combo_manager
        
        self.setup()
        self.set_table()
        self.populate_combos()
        self.deselection()

    def set_table(self):
        self.model = create_table_model(TableType.CLASSES)
        self.class_table.setModel(self.model)
        self.class_table.hideColumn(self.model.ID_COLUMN)
        set_header_resize_mode(self.class_table, self.model)
    
    def setup(self):
        self.add_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete_class)
        self.class_table.doubleClicked.connect(self.select_row)
        self.search.textChanged.connect(self.show_class)
        self.reset_btn.clicked.connect(self.reset)
        self.teacher_search.currentTextChanged.connect(self.show_class)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def aquire_data(self, action: WorkingMode):
        dialog = create_popup_factory(
            kind=PopupKind.CLASSES, 
            title="إضافة قسم" if action == WorkingMode.ADD else "تعديل قسم", 
            parent=self
        )
        if action == WorkingMode.UPDATE:
            if self.identifier is None:
                error("يرجى تحديد قسم")
                return
            data = self.manager.get_by_id(self.identifier)
            dialog.content.repopulate_fields(data.__dict__)
            
        def on_confirm():
            data = dialog.content.get_data()
            self.control(action, data)
            
        dialog.confirmed.connect(on_confirm)
        dialog.show()

    def control(self, action: WorkingMode, data):
        entity = SchemaFactory.CLASSES(
            name=data["name"],
            way=data["way"],
            teacher=data["teacher"],
            note=data["note"],
            price=data["price"],
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
            self.manager.create(entity)
        elif action == WorkingMode.UPDATE:
            self.manager.update(self.identifier, entity)
            self.deselection()
            
        self.show_class()
        self.combo_manager.update_cache_from_db(data_name=ComboName.CLASS)
        
    def selection(self, identifier):
        self.identifier = identifier
        self.select_info.setStyleSheet(get_selection_status_stylesheet(True))
        
    def deselection(self):
        self.identifier = None
        self.select_info.setStyleSheet(get_selection_status_stylesheet(False))
        
    def select_row(self, index):
        row_index = index.row()    

        identifier = self.model.data(self.model.index(row_index, 0), role=0)
        
        self.selection(identifier)

    def delete_class(self):
        if self.identifier is None:
            error("يرجى تحديد قسم")
            return
        
        self.manager.sup_security(widget=self, id=self.identifier, text="متأكد من حذف هذا القسم ؟")
        self.combo_manager.update_cache_from_db("classes")
        self.show_class()
        self.deselection()

    def show_class(self):
        name = self.search.text()
        teacher = self.teacher_search.currentText()

        if name == "":
            name = None

        if teacher == "":
            teacher = None

        filters = self.manager.get_filters(name=name, teacher=teacher)

        data = self.manager.get_by_filter(filters)
        self.model.refresh(data)

        self.nb.setText(str(self.model.rowCount()))       

    def populate_combos(self):
        self.combo_manager.update_combo(self.teacher_search, ComboName.TEACHER)

    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(data_to_export, row_count)
        
        self.manager.export_data(report_type=output_channel, parent=self)
        
    def reset(self):
        self.search.setText("")
        self.teacher_search.setCurrentIndex(-1)
        self.show_class()

class ClasseleveLogic(QWidget, ClasseleveUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.CLASSES, "classeleve.ui", self)

        self.model = None
        self.model_classeleve = None
        
        self.manager = get_model(ModelName.ENROLLMENT)
        self.classes_manager = get_model(ModelName.CLASSES)
        self.combo_manager = get_combo_manager

        self.set_table()
        self.populate_combo()
        self.show_students_list()

        self.setup()

    def setup(self):
        self.student_search_list.doubleClicked.connect(self.add)
        self.students.doubleClicked.connect(self.delete)
        self.student_search.textChanged.connect(self.show_students_list)
        self.search_btn.clicked.connect(self.show_classeleve)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def set_table(self):
        self.setup_classeleve()
        self.setup_students()

    def setup_classeleve(self):
        self.model_classeleve = create_table_model(TableType.CLASS_ENROLLMENT)

        self.students.setModel(self.model_classeleve)

    def setup_students(self):
        self.model = create_table_model(TableType.STUDENT_SEARCH)

        self.student_search_list.setModel(self.model)
        
        self.student_search_list.hideColumn(self.model.ID_COLUMN)

    def add(self, index=None):
        if index is None:
            index = self.student_search_list.selectionModel().selectedRows()[0]
        
        row_index = index.row()
        
        class_name = self.classes.currentText()
        student_id = self.model.data(self.model.index(row_index, 0), role=0)

        if class_name == "":
            error("يرجى اختيار صف")
            return
        
        if self.manager.check(student_id, class_name):
            print(f"Student {student_id} is already enrolled in class {class_name}")
            error("هذا التلميذ موجود في هذا الصف")
            return
        
        entity = SchemaFactory.ENROLLMENT(
            student_id=student_id,
            class_name=class_name,
            user=get_username()
        )
        
        if not entity.validate():
            error("الرجاء ملء جميع الحقول")
            return
        
        try:
            self.manager.create(entity)
            self.show_classeleve()
        except IntegrityError as e:
            error("هذا التلميذ موجود في هذا الصف")
            return

    def delete(self, index=None):
        line = self.model_classeleve.data(self.model_classeleve.index(index.row(), 0), role=0)
        if self.classes.currentText() == "تأمين":
            error("لا يمكن حذف تلميذ من الصف تأمين")
            return
        try:
            self.manager.sup_security(widget=self, id=line, text="متأكد من حذف هذا التلميذ من الصف ؟")
            self.show_classeleve()
        except ValueError as e:
            error(str(e))
            return      

    def show_classeleve(self):
        class_name = self.student_search.text()
        if class_name == "":
            class_name = None

        if self.classes.currentText() != "":
            class_name = self.classes.currentText()
            
        filters = self.manager.get_filters(class_name=class_name)
        
        students = self.manager.get_with_joined_load(relationship_name="students", filters=filters)
        
        self.model_classeleve.refresh(students)

        self.nb.setText(str(self.model_classeleve.rowCount()))
        

    def show_students_list(self, student = ""):

        students = get_student_list(student)
        
        self.model.refresh(students)

    def reset(self):
        self.classes.setCurrentIndex(-1)

    def populate_combo(self):
        self.combo_manager.update_combo(self.classes, ComboName.CLASS)
        
    def export(self, output_channel: ReportType):
        data_to_export = self.model_classeleve.get_current_data()
        row_count = self.model_classeleve.rowCount()
        class_name = self.classes.currentText()
        filters = self.classes_manager.get_filters(name=class_name)
        teacher = self.classes_manager.get_by_filter(filters)[0].teacher
        
        self.manager.set_dynamic_metadata(
            data_to_export=data_to_export, 
            row_count=row_count, 
            class_name=class_name,
            teacher=teacher
            )
        
        self.manager.export_data(
            report_type=output_channel,
            parent=self
        )

if __name__ == "__main__":
    app = QApplication([])
    window = ClassesLogic()
    window.show()
    app.exec()