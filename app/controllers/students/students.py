from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import QDate, QPropertyAnimation, QEasingCurve
from app.models import ModelName, get_model
from sqlalchemy.exc import IntegrityError
from app.view import TableType, create_table_model
from os import path
from app.repo.schemas import SchemaFactory
from app.utils import (
    error, 
    get_username,
    get_combo_manager,
    ReportType,
    load_gui,
    WorkingMode,
    UiPath
)
from app.ui.ui_forms import StudentsUI, StudentHistoryUI, ClassesPerStudentUI
from app.controllers.popup import create_popup_factory, PopupKind

class StudentsLogic(QWidget, StudentsUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        load_gui(UiPath.STUDENTS, "students.ui", self)

        self.identifier = None
        self.model = None
        
        self.manager = get_model(ModelName.STUDENT)
        self.enrollment_manager = get_model(ModelName.ENROLLMENT)
        self.history_manager = get_model(ModelName.STUDENT_HISTORY)
        self.combo_manager = get_combo_manager()

        self.to.setDate(QDate.currentDate())
        self.du.setDate(QDate.currentDate())
        self.gender_search.setCurrentIndex(-1)

        self.animation = QPropertyAnimation(self.search_frame, b"maximumWidth")
        self.animation.setDuration(500)  # 500ms animation
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.search_section("minimize")

        self.setup_table()

        self.setup()

    def setup(self):
        self.add_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete)
        self.minimize.clicked.connect(lambda: self.search_section("minimize"))
        self.maximize.clicked.connect(lambda: self.search_section("maximize"))
        self.reset_btn.clicked.connect(self.reset_filters)
        self.student_tab.doubleClicked.connect(self.select_student)
        self.search_btn.clicked.connect(self.show_table)
        self.new_year.clicked.connect(self.set_new_year)
        self.printing_btn.clicked.connect(lambda: self.export(output_channel=ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(output_channel=ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.STUDENTS)

        self.student_tab.setModel(self.model)
        self.student_tab.hideColumn(self.model.ID_COLUMN)

    def aquire_data(self, action:WorkingMode):
        dialog = create_popup_factory(
            kind=PopupKind.STUDENT,
            title="إضافة تلميذ" if action == WorkingMode.ADD else "تعديل تلميذ",
            parent=self
        )
        
        if action == WorkingMode.UPDATE:
            if self.identifier is None:
                error("يرجى تحديد التلميذ")
                return
            data = self.manager.get_by_id(self.identifier)
            dialog.content.repopulate_fields(data.__dict__)
        def on_confirmed():
            data = dialog.content.get_data()
            self.controls(action, data)
            
        dialog.confirmed.connect(on_confirmed)
        dialog.show()

    def controls(self, action, data): 
        name, parent, _date = data["name"], data["parent"], data["date_inscrit"]
        if action == WorkingMode.ADD:
            if self.manager.exists(name, parent):
                error("التلميذ موجود")
                return

        entity = SchemaFactory.STUDENT(
            name=name,
            birthday=data["birthday"],
            date_inscrit=data["date_inscrit"],
            note=data["note"],
            user=get_username(),
            gender=data["gender"],
            parent=parent,
            cin=data["cin"],
            activity=data["activity"],
            num_tel=f"{data['num_tel']}/{data['num_tel_2']}" if data['num_tel_2'] else data['num_tel'],
            excused=data["excused"]
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
                with self.manager.transaction():
                    self.manager.create(entity)
                    student_id = self.manager.get_last_student().id
                    self.add_ensurance(student_id, "تأمين")
                    self.add_history(student_id, _date)
            except Exception as e:
                error(str(e))
                return
        else:
            try:
                self.manager.update(id=self.identifier, data_obj=entity)
                self.identifier = None
            except Exception as e:
                error(str(e))
                return

        self.show_table()
    
    def add_ensurance(self, student_id, class_name):
        ensurance = SchemaFactory.ENROLLMENT(
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
            self.enrollment_manager.create(ensurance)
        except IntegrityError as e:
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

    def delete(self):
        self.manager.sup_security(id=self.identifier, text="متأكد من حذف هذا التلميذ ؟")
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
                with self.manager.transaction():
                    old_date = student.date_inscrit
                    student.date_inscrit = QDate.currentDate().toPyDate()
                    self.add_history(self.identifier, old_date)
            except Exception:
                error("هذا التلميذ موجود.")

        else:	
            error("هذا التلميذ غير موجود.")

        self.identifier = None
        self.show_table()
    
    def add_history(self, student_id, date): 
        entity = SchemaFactory.STUDENT_HISTORY(
            num_inscrit=student_id,
            date_inscrit= date,
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
        except IntegrityError as e:
            error("لم تتم الاضافة")

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
        
    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(
            data_to_export=data_to_export, 
            row_count=row_count
            )
        
        self.manager.export_data(
            report_type=output_channel,
            parent=self
        )

class StudentsHistoryLogic(QWidget, StudentHistoryUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.STUDENTS, "students_history.ui", self)

        self.model = None
        
        self.manager = get_model(ModelName.STUDENT_HISTORY)

        self.setup_table()

        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(lambda: self.num_ins_search.setText(""))
        self.printing_btn.clicked.connect(lambda: self.export(output_channel=ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(output_channel=ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.STUDENT_HISTORY)

        self.student_tab.setModel(self.model)
        self.student_tab.hideColumn(self.model.ID_COLUMN)

    def search(self):
        identifier = self.num_ins_search.text()
        if identifier == "":
            self.model.refresh([])
            return
            
        try:
            student_id = int(identifier)
        except ValueError:
            self.model.refresh([])
            return

        history_records = self.manager.search_by_num_inscrit(student_id)

        self.model.refresh(history_records)
        
    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(
            data_to_export=data_to_export, 
            row_count=row_count
            )
        
        self.manager.export_data(
            report_type=output_channel,
            parent=self
        )

class ClassesPerStudentLogic(QWidget, ClassesPerStudentUI):
    def __init__(self, parent = None):
        super().__init__(parent)

        load_gui(UiPath.CLASSES, "classes_per_student.ui", self)

        self.model = None
        self.name = ""
        
        self.enrollment_manager = get_model(ModelName.ENROLLMENT)
        self.student_manager = get_model(ModelName.STUDENT)
        
        self.setup_table()
        self.setup()

    def setup(self):
        self.reset_btn.clicked.connect(self.reset)
        self.search_ent.textChanged.connect(self.student_search)
        self.student_list.doubleClicked.connect(self.list_of_classes)

    def setup_table(self):
        self.model = create_table_model(TableType.STUDENT_SEARCH)

        self.student_list.setModel(self.model)
        self.student_list.hideColumn(self.model.ID_COLUMN)
        
    def student_search(self):
        name = self.search_ent.text()
        filters = self.student_manager.get_filters(name=name)
        students = self.student_manager.get_by_filter(filters)
        self.model.refresh(students)

    def get_id(self):
        row = self.student_list.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()

        self.name = self.model.data(self.model.index(row_index, 1), role=0)	

        return self.model.data(self.model.index(row_index, 0), role=0)

    def list_of_classes(self):
        id = self.get_id()
        
        filters = self.enrollment_manager.get_filters(student_id=id, not_class_name="تأمين")
        classes = self.enrollment_manager.get_by_filter(filters)

        self.class_list.clear()

        if classes:
            for class_name in classes:
                self.class_list.addItem(class_name[0])

        else:
            error("لا يوجد صفوف لهذا التلميذ")

    def reset(self):
        self.search_ent.setText("")
        self.class_list.clear()

if __name__ == '__main__':
    app = QApplication([])
    window = StudentsLogic()
    window.show()
    app.exec() 
