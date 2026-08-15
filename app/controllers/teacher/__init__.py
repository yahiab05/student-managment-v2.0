from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.uic import loadUi
from os import path

from app.controllers.teacher.teachers import TeacherLogic, TeachersHistoryLogic
from app.ui.ui_forms import TeacherPartUI

class TeachersPart(QWidget, TeacherPartUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = path.abspath("../../ui/teacher_part.ui")
        loadUi(ui_path, self)

        self.t = TeacherLogic(self)
        self.th = TeachersHistoryLogic(self)

        self.stackedWidget.addWidget(self.t)
        self.stackedWidget.addWidget(self.th)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.teacher)

        self.setup()

    def setup(self):
        self.teacher.clicked.connect(self.go_to_teachers)
        self.teacher_history.clicked.connect(self.go_to_history)

    def go_to_teachers(self):
        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.teacher)

    def go_to_history(self):
        self.stackedWidget.setCurrentIndex(1)
        self.th.setup_table()
        self.buttons(self.teacher_history)

    def buttons(self, button:QPushButton): 
        self.teacher.setStyleSheet("color: white")
        self.teacher_history.setStyleSheet("color: white")

        button.setStyleSheet("color: green")