from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDate

from app.ui.ui_forms import ViewNotPayedUI as V
from app.utils import error, get_combo_manager, load_gui, UiPath
from app.models import get_model, ModelName


class ViewNotPayedLogic(QWidget, V):
    def __init__(self, parent = None):
        super().__init__(parent)

        load_gui(UiPath.PAYMENTS, "not_payed.ui", self)

        self.manager = get_model(ModelName.PAYMENTS)
        self.enrollment_manager = get_model(ModelName.ENROLLMENT)
        self.combo_manager = get_combo_manager()

        self.month.setValue(1)
        self.year.setValue(QDate.currentDate().year())

        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(self.reset)

    def search(self):
        class_ = self.classroom.currentText()
        if not class_:
            error("يرجى تحديد الصف")
            return

        elif class_ == "تأمين":
            filters = self.manager.get_filter(classroom=class_, year=year)
            data = self.manager.get_by_filter(filters)
            
            query = [student.num_inscrit for student in data]

            filters = self.enrollment_manager.get_filters(not_included=query, activity="فاعل")
            students = self.enrollment_manager.get_by_filter(filters)
            
            self.tbl.clear()

            for s in students:
                self.tbl.addItem(s.name)

        else:
            month = self.month.value()
            year = self.year.value()
            
            filters = self.manager.get_filter(classroom=class_, year=year, month=month)
            data = self.manager.get_by_filter(filters)

            query = [student.num_inscrit for student in query]

            filters = self.enrollment_manager.get_filters(
                not_included=query, classroom=class_, not_included=query
                )
            
            students = self.enrollment_manager.get_by_filter(filters)

            self.tbl.clear()

            for s in students:
                self.tbl.addItem(s.students.name)

    def reset(self):
        self.classroom.setCurrentIndex(-1)
        self.month.setValue(1)
        self.year.setValue(QDate.currentDate().year())

    def populate_classes(self):
        self.combo_manager.update_combo(self.classroom, ModelName.CLASSES)