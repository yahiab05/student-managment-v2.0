from PyQt6.QtWidgets import QWidget

from app.ui.ui_forms import StudentPartUI
from .students import StudentsLogic, StudentsHistoryLogic, ClassesPerStudentLogic
from app.utils import load_gui, UiPath, buttons

class StudentsPart(QWidget, StudentPartUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_gui(UiPath.STUDENTS, "studentpart.ui", self)

        self.s = StudentsLogic(self)
        self.sh = StudentsHistoryLogic(self)
        self.cps = ClassesPerStudentLogic(self)

        self.stackedWidget.addWidget(self.s)
        self.stackedWidget.addWidget(self.sh)
        self.stackedWidget.addWidget(self.cps)

        self.stackedWidget.setCurrentIndex(0)
        buttons(self, self.students, self.students_history, self.classes_per_student)

        self.setup()

    def setup(self):
        self.students.clicked.connect(self.go_to_students)
        self.students_history.clicked.connect(self.go_to_history)
        self.classes_per_student.clicked.connect(self.go_to_classes_per_student)

    def go_to_students(self):
        self.stackedWidget.setCurrentIndex(0)
        buttons(self, self.students, self.students_history, self.classes_per_student)

    def go_to_history(self):
        self.stackedWidget.setCurrentIndex(1)
        self.sh.setup_table()
        buttons(self, self.students_history, self.students, self.classes_per_student)

    def go_to_classes_per_student(self):
        self.stackedWidget.setCurrentIndex(2)
        self.cps.setup_table()
        buttons(self, self.classes_per_student, self.students, self.students_history)