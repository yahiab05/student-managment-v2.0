from PyQt6.QtWidgets import QWidget

from app.controllers.classes.classes import ClassesLogic, ClasseleveLogic
from app.ui.ui_forms import ClassPartUI
from app.utils import load_gui, UiPath, buttons

class ClassPart(QWidget, ClassPartUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.CLASSES, "class_part.ui", self)

        self.c = ClassesLogic(self)
        self.ce = ClasseleveLogic(self)

        self.stackedWidget.addWidget(self.c)
        self.stackedWidget.addWidget(self.ce)

        self.stackedWidget.setCurrentIndex(0)
        
        buttons(self, self.classes, self.classeleve)

        self.setup()

    def setup(self):    
        self.classes.clicked.connect(self.go_to_classes)
        self.classeleve.clicked.connect(self.go_to_classeleve)

    def go_to_classes(self):
        self.stackedWidget.setCurrentIndex(0)
        self.c.populate_combos()
        buttons(self, self.classes, self.classeleve)

    def go_to_classeleve(self):
        self.stackedWidget.setCurrentIndex(1) 
        self.ce.populate_combo()
        buttons(self, self.classeleve, self.classes)
