from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.uic import loadUi
from os import path

from app.ui.ui_forms import StudentPartUI
from .students import StudentsLogic, StudentsHistoryLogic, ClassesPerStudentLogic


class StudentsPart(QWidget, StudentPartUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = path.abspath("../../ui/studentpart.ui")  # Convert to absolute path

        loadUi(ui_path, self)

        self.s = StudentsLogic(self)
        self.sh = StudentsHistoryLogic(self)
        self.cps = ClassesPerStudentLogic(self)

        self.stackedWidget.addWidget(self.s)
        self.stackedWidget.addWidget(self.sh)
        self.stackedWidget.addWidget(self.cps)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.students)

        self.setup()

    def setup(self):
        self.students.clicked.connect(self.go_to_students)
        self.students_history.clicked.connect(self.go_to_history)
        self.classes_per_student.clicked.connect(self.go_to_classes_per_student)

    def go_to_students(self):
        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.students)

    def go_to_history(self):
        self.stackedWidget.setCurrentIndex(1)
        self.sh.setup_table()
        self.buttons(self.students_history)

    def go_to_classes_per_student(self):
        self.stackedWidget.setCurrentIndex(2)
        self.cps.setup_table()
        self.buttons(self.classes_per_student)

    def buttons(self, button:QPushButton):
        self.students.setStyleSheet("color: white")
        self.students_history.setStyleSheet("color: white")
        self.classes_per_student.setStyleSheet("color: white")

        button.setStyleSheet("color: green")