import os
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from sqlalchemy.exc import IntegrityError

from ..repo.database import SessionLocal
from ..view.classes_tables import ClassesTableModel, ClasseleveTableModel
from ..view.students_tables import StudentsSearchTableModel
from ..models.classes import Classes, Enrollment
from ..repo.schemas import SchemaFactory
from ..utils.utils import error, get_student_list
from ..utils.combo_manager import ComboManager

class ClassesLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.abspath("./ui/classes.ui")

        loadUi(ui_path, self)

        self.model = None

        self.identifier = 0
        
        session = SessionLocal()
        
        self.manager = Classes(session)
        self.combo_manager = ComboManager(session)
        
        self.setup()
        self.set_table()
        self.populate_combos()

    def set_table(self):
        session = SessionLocal()
        self.model = ClassesTableModel(session)
        self.class_table.setModel(self.model)
        session.close()


    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.delete_class)
        self.class_table.doubleClicked.connect(self.select_row)
        self.search.textChanged.connect(self.show_class)
        self.teacher_search.currentTextChanged.connect(self.show_class)
        self.printing_btn.clicked.connect(lambda: self.export("print"))
        self.export_btn.clicked.connect(lambda: self.export("excel"))

    def control(self, action):
        name = self.name.text()
        way = self.way.currentText()
        teacher = self.teacher.currentText()
        note = self.note.text()
        price = self.price.text()
        exchange = self.in_exchange.currentText()
        teacher_part = self.teacher_price.value()
        seance = self.seance.value()

        entity = SchemaFactory.CLASSES.create(
            name=name,
            way=way,
            teacher=teacher,
            note=note,
            price=price,
            exchange=exchange,
            teacher_part=teacher_part,
            seance=seance
        )
        try:
            if not entity.validate():
                error("الرجاء ملء جميع الحقول")
                return
        except ValueError as e:
            error(str(e))
            return

        if action == "add":
            self.manager.create(entity)
        elif action == "update":
            self.manager.update(self.identifier, entity)
            
        self.reset()
        self.show_class()
        self.combo_manager.update_cache_from_db("classes")

    def select_row(self):
        row = self.class_table.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد قسم")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)

        self.repopulate()

    def repopulate(self):
        if self.identifier is None:
            error("يرجى تحديد قسم")
            return
        data = self.manager.get_by_id(self.identifier)

        if data is not None:
            self.name.setText(data.name)
            self.way.setCurrentText(data.way)
            self.teacher.setCurrentText(data.teacher)
            self.note.setText(data.note)
            self.price.setText(str(data.price))
            self.in_exchange.setCurrentText(data.exchange)
            self.teacher_price.setValue(data.teacher_part)
            self.seance.setValue(data.seance)

    def delete_class(self):
        self.manager.sup_security(self.identifier)

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

    def reset(self):
        self.name.setText("")
        self.way.setCurrentIndex(-1)
        self.teacher.setCurrentIndex(-1)
        self.note.setText("")
        self.price.setText("")
        self.in_exchange.setCurrentIndex(-1)
        self.teacher_price.setValue(0)
        self.seance.setValue(0)


    def populate_combos(self):
        teachers = self.combo_manager.get_cached_data("teachers")
        ways = self.combo_manager.get_cached_data("way teaching")

        for teacher in teachers:
            self.teacher.addItem(teacher[0])
            self.teacher_search.addItem(teacher[0])

        for way in ways:
            self.way.addItem(way[0])

        self.teacher.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.teacher_search.setCurrentIndex(-1)

    def export(self, output_channel: str):
        data_to_export = self.model.get_current_data()
        row_count = self.model.rowCount()
        self.manager.set_dynamic_metadata(data_to_export, row_count)
        
        if output_channel == "print":
            self.printing_preview()
        elif output_channel == "excel":
            self.excel()
        else:
            ValueError(f"Unknown output channel: {output_channel}")
            
    def printing_preview(self):
        try:
            self.manager.print_preview(self)
        except Exception as e:
            error("لا يمكنك الطباعة")

    def excel(self):
        try:
            self.manager.excel(self)
        except Exception as e:
            error("لا يمكنك تحميل الملف")


class ClasseleveLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.abspath("./ui/classeleve.ui")
        loadUi(ui_path, self)

        self.model = None
        self.model_classeleve = None
        
        session = SessionLocal()
        self.manager = Enrollment(session)
        self.combo_manager = ComboManager(session)

        self.setup_students()
        self.setup_classeleve()
        self.populate_combo()

        self.setup()

    def setup(self):
        self.student_search_list.doubleClicked.connect(self.add)
        self.students.doubleClicked.connect(self.sup_security)
        self.student_search.textChanged.connect(self.show_students_list)
        self.search_btn.clicked.connect(self.show_classeleve)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(lambda: self.export("print"))
        self.export_btn.clicked.connect(lambda: self.export("excel"))

        self.classes.setCurrentIndex(-1)

    def setup_classeleve(self):
        session = SessionLocal()

        self.model_classeleve = ClasseleveTableModel(session)

        self.students.setModel(self.model_classeleve)

        session.close()

    def setup_students(self):
        session = SessionLocal()

        self.model = StudentsSearchTableModel(session)

        self.student_search_list.setModel(self.model)

        session.close()

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
        
        entity = SchemaFactory.ENROLLMENT.create(
            student_id=student_id,
            class_name=class_name
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
        classes = self.combo_manager.get_cached_data("classes")

        for class_name in classes:
            self.classes.addItem(class_name[0])

        self.classes.setCurrentIndex(-1)
        
    def export(self, output_channel: str):
        data_to_export = self.model_classeleve.get_current_data()
        row_count = self.model_classeleve.rowCount()
        class_name = self.classes.currentText()
        self.manager.set_dynamic_metadata(
            data_to_export=data_to_export, 
            row_count=row_count, 
            class_name=class_name
            )
        
        if output_channel == "print":
            self.printing_preview()
        elif output_channel == "excel":
            self.excel()
        else:
            ValueError(f"Unknown output channel: {output_channel}")
            
    def printing_preview(self):
        try:
            self.manager.print_preview(self)
        except Exception as e:
            error("لا يمكنك الطباعة")

    def excel(self):
        try:
            self.manager.export_to_excel(self)
        except Exception as e:
            error("لا يمكنك تحميل الملف")

if __name__ == "__main__":
    app = QApplication([])
    window = ClassesLogic()
    window.show()
    app.exec()