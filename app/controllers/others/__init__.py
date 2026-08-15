from admin import UserLogic, RoleLogic
from settings import SettingsLogic

from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.uic import loadUi
from os import path

from app.ui.ui_forms import UserPartUI

class UserPart(QWidget, UserPartUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        ui_path = path.abspath("../../ui/user_part.ui")   
        loadUi(ui_path, self)

        self.u = UserLogic(self)
        self.r = RoleLogic(self)

        self.stackedWidget.addWidget(self.u)
        self.stackedWidget.addWidget(self.r)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.user)

        self.setup()

    def setup(self):
        self.user.clicked.connect(self.go_to_users)
        self.add_role.clicked.connect(self.go_to_roles)

    def go_to_users(self):
        self.stackedWidget.setCurrentIndex(0)
        self.u.populate_combo()
        self.buttons(self.user)

    def go_to_roles(self):
        self.stackedWidget.setCurrentIndex(1)
        self.buttons(self.add_role)

    def buttons(self, button:QPushButton):
        self.user.setStyleSheet("color: white")
        self.add_role.setStyleSheet("color: white")

        button.setStyleSheet("color: green")

# THe settings part is added from another file