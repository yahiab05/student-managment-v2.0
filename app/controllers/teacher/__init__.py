from PyQt6.QtWidgets import QWidget

from app.controllers.teacher.teachers import TeacherLogic, TeachersHistoryLogic
from app.ui.ui_forms import TeacherPartUI
from app.utils import load_gui, UiPath, buttons

class TeachersPart(QWidget, TeacherPartUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.TEACHERS, "teacher_part.ui", self)

        self.t = TeacherLogic(self)
        self.th = TeachersHistoryLogic(self)

        self.stackedWidget.addWidget(self.t)
        self.stackedWidget.addWidget(self.th)

        self.stackedWidget.setCurrentIndex(0)
        buttons(self, self.teacher, self.teacher_history)

        self.setup()

    def setup(self):
        self.teacher.clicked.connect(self.go_to_teachers)
        self.teacher_history.clicked.connect(self.go_to_history)

    def go_to_teachers(self):
        self.stackedWidget.setCurrentIndex(0)
        buttons(self, self.teacher, self.teacher_history)

    def go_to_history(self):
        self.stackedWidget.setCurrentIndex(1)
        self.th.setup_table()
        buttons(self, self.teacher_history, self.teacher)