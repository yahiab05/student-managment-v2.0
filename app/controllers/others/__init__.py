from .admin import UserLogic, RoleLogic
from .settings import (SettingsUI, WaySettings, IncomeSettings, 
                        ExpenseSettings, PaymentSettings, FournisseurSettings)

from PyQt6.QtWidgets import QWidget, QPushButton

from app.ui.ui_forms import UserPartUI
from app.utils import load_gui, UiPath, buttons

class UserPart(QWidget, UserPartUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        load_gui(UiPath.OTHERS, "user_part.ui", self)

        self.u = UserLogic(self)
        self.r = RoleLogic(self)

        self.stackedWidget.addWidget(self.u)
        self.stackedWidget.addWidget(self.r)

        self.stackedWidget.setCurrentIndex(0)
        buttons(self, self.user, self.add_role)

        self.setup()

    def setup(self):
        self.user.clicked.connect(self.go_to_users)
        self.add_role.clicked.connect(self.go_to_roles)

    def go_to_users(self):
        self.stackedWidget.setCurrentIndex(0)
        self.u.populate_combo()
        buttons(self, self.user, self.add_role)

    def go_to_roles(self):
        self.stackedWidget.setCurrentIndex(1)
        buttons(self, self.add_role, self.user)

class SettingsLogic(QWidget, SettingsUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        load_gui(UiPath.OTHERS, "settings.ui", self)

        self.setup()

    def setup(self):
        settings = [
            WaySettings(parent=self.plane),
            IncomeSettings(parent=self.plane),
            ExpenseSettings(parent=self.plane),
            PaymentSettings(parent=self.plane),
            FournisseurSettings(parent=self.plane)
        ]
        buttons = [
            self.way_btn,
            self.income_btn,
            self.expense_btn,
            self.payment_btn,
            self.fr_btn
        ]
        for i in range(len(settings)):
            self.plane.addWidget(settings[i])
            buttons[i].clicked.connect(
                lambda checked=False, i=i: self.plane.setCurrentWidget(settings[i])
                )
        self.plane.setCurrentWidget(settings[0])