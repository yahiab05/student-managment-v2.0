import os
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
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
    ComboName
)
from app.ui.ui_forms import ClassesUI, ClasseleveUI

class ClassesLogic(QWidget, ClassesUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui", "classes", "classes.ui"))

        loadUi(ui_path, self)

        self.model = None

        self.identifier = 0
        
        self.manager = get_model(ModelName.CLASSES)
        self.combo_manager = get_combo_manager()
        
        self.setup()
        self.set_table()
        self.populate_combos()

    def set_table(self):
        self.model = create_table_model(TableType.CLASSES)
        self.class_table.setModel(self.model)
        self.class_table.hideColumn(self.model.ID_COLUMN)


    def setup(self):
        self.add_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete_class)
        self.class_table.doubleClicked.connect(self.select_row)
        self.search.textChanged.connect(self.show_class)
        self.teacher_search.currentTextChanged.connect(self.show_class)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def aquire_data(self, action: WorkingMode):
        dialog = create_popup_factory(
            kind=PopupKind.CLASS_FORM, 
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
            
        self.show_class()
        self.combo_manager.update_cache_from_db(combo_name=ComboName.CLASS)

    def select_row(self):
        row = self.class_table.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد قسم")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)

    def delete_class(self):
        self.manager.sup_security(self.identifier)
        self.combo_manager.update_cache_from_db("classes")

    def show_class(self):
        name = self.search.text()
        teacher = self.teacher_search.currentText()

        if name == "":
            name = None

        if teacher == "":
            teacher = None

        filters = self.manager.get_data_using_filters(name=name, teacher=teacher)

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

class ClasseleveLogic(QWidget, ClasseleveUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui", "classes", "classeleve.ui"))
        loadUi(ui_path, self)

        self.model = None
        self.model_classeleve = None
        
        self.manager = get_model(ModelName.ENROLLMENT)
        self.combo_manager = get_combo_manager()

        self.set_table()
        self.populate_combo()

        self.setup()

    def setup(self):
        self.student_search_list.doubleClicked.connect(self.add)
        self.students.doubleClicked.connect(self.sup_security)
        self.student_search.textChanged.connect(self.show_students_list)
        self.search_btn.clicked.connect(self.show_classeleve)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

        self.classes.setCurrentIndex(-1)

    def set_table(self):
        self.setup_classeleve()
        self.setup_students()

    def setup_classeleve(self):
        self.model_classeleve = create_table_model(TableType.CLASS_ENROLLMENT)

        self.students.setModel(self.model_classeleve)

    def setup_students(self):
        self.model = create_table_model(TableType.STUDENT_SEARCH)

        self.student_search_list.setModel(self.model)

    def get_student_id(self):
        row = self.student_search_list.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()    

        identifier = self.model.data(self.model.index(row_index, 0), role=0)

        return identifier

    def add(self):
        class_name = self.classes.currentText()

        if class_name == "":
            error("يرجى اختيار صف")
            return

        student_id = self.get_student_id()

        if not self.manager.check(student_id, class_name):
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
        except IntegrityError:
            error("هذا التلميذ موجود في هذا الصف")
            return
        finally:
            pass # Replace it with refreshing the table

    def sup_security(self):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا التلميذ ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            line = self.line_to_delete()
            try:
                self.manager.delete(line)
                self.show_classeleve()
            except ValueError as e:
                error(str(e))
                return

    def line_to_delete(self):
        row = self.students.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()    

        identifier = self.model_classeleve.data(self.model_classeleve.index(row_index, 0), role=0)

        return identifier        

    def show_classeleve(self):
        class_name = self.student_search.text()
        if class_name == "":
            class_name = None

        if self.classes.currentText() != "":
            class_name = self.classes.currentText()
            
        filters = self.manager.get_filters(class_name=class_name)
        students = self.manager.get_by_filter(filters)
        
        self.model_classeleve.refresh(students)

        self.nb.setText(str(self.model_classeleve.rowCount()))
        

    def show_students_list(self, student = ""):

        students = get_student_list(student)
        
        self.model.refresh(students)

    def reset(self):
        self.classes.setCurrentIndex(-1)

    def populate_combo(self):
        classes = self.combo_manager.get_cached_data(data_name=ComboName.CLASS)

        for class_name in classes:
            self.classes.addItem(class_name[0])

        self.classes.setCurrentIndex(-1)
        
    def export(self, output_channel: ReportType):
        data_to_export = self.model_classeleve.get_current_data()
        row_count = self.model_classeleve.rowCount()
        class_name = self.classes.currentText()
        self.manager.set_dynamic_metadata(
            data_to_export=data_to_export, 
            row_count=row_count, 
            class_name=class_name
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