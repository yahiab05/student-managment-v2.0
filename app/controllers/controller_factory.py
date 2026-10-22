from enum import StrEnum, auto
from app.controllers.classes import ClassPart
from app.controllers.finance import MoneyPart
from app.controllers.students import StudentsPart
from app.controllers.teacher import TeachersPart
from app.controllers.payment import PaymentPart
from app.controllers.others import SettingsLogic, UserPart

from PyQt6.QtWidgets import QStackedWidget, QPushButton, QWidget


class ControllerSection(StrEnum):
    STUDENTS = auto()
    TEACHERS = auto()
    CLASSES = auto()
    FINANCE = auto()
    PAYMENTS = auto()
    ADMIN = auto()
    SETTINGS = auto()
    

class ControllerFactory:
    def __init__(self):
        self.controller = {
            ControllerSection.STUDENTS: StudentsPart,
            ControllerSection.TEACHERS: TeachersPart,
            ControllerSection.CLASSES: ClassPart,
            ControllerSection.PAYMENTS: PaymentPart,
            ControllerSection.FINANCE: MoneyPart,
            ControllerSection.ADMIN: UserPart,
            ControllerSection.SETTINGS: SettingsLogic
        }
        
    def create_controller(self, section: ControllerSection) -> QWidget:
        controller_class = self.controller.get(section)
        if controller_class:
            return controller_class()
        else:
            raise ValueError(f"No controller found for section: {section}")
        
    def setup_sections(self, stacked_widget:QStackedWidget, buttons: dict[ControllerSection, QPushButton]):
        for section in self.controller.keys():
            controller_instance = self.create_controller(section)
            stacked_widget.addWidget(controller_instance)
            buttons[section].clicked.connect(
                lambda checked= False, instance=controller_instance: self.switch_section(stacked_widget, instance)
                )
            
    def switch_section(self, stacked_widget:QStackedWidget, section:QWidget):
        stacked_widget.setCurrentWidget(section)
