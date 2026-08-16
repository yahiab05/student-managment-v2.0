from PyQt6.QtWidgets import QWidget, QPushButton

from app.controllers.classes.classes import ClassesLogic, ClasseleveLogic
from app.ui.ui_forms import ClassPartUI
from app.utils import load_gui, UiPath

class ClassPart(QWidget, ClassPartUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.CLASSES, "class_part.ui", self)

        self.c = ClassesLogic(self)
        self.ce = ClasseleveLogic(self)

        self.stackedWidget.addWidget(self.c)
        self.stackedWidget.addWidget(self.ce)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.classes)

        self.setup()

    def setup(self):    
        self.classes.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.classeleve.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def go_to_classes(self):
        self.stackedWidget.setCurrentIndex(0)
        self.c.populate_combos()
        self.buttons(self.classes)

    def go_to_classeleve(self):
        self.stackedWidget.setCurrentIndex(1) 
        self.buttons(self.classeleve)
        self.ce.populate_combo()

    def buttons(self, button:QPushButton):
        self.classes.setStyleSheet("color: white")
        self.classeleve.setStyleSheet("color: white")

        button.setStyleSheet("color: green")
