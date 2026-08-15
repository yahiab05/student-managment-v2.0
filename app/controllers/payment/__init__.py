from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.uic import loadUi
from os import path

from app.controllers.payment.payments import ViewPayment
from app.controllers.payment.not_payed_view import ViewNotPayedLogic

from app.ui.ui_forms import PaymentPartUI

class PaymentPart(QWidget, PaymentPartUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        ui_path = path.abspath("./ui/payment_part.ui")  # Convert to absolute path

        loadUi(ui_path, self)

        self.vp = ViewPayment()
        self.vnp = ViewNotPayedLogic()

        self.stackedWidget.addWidget(self.vp)
        self.stackedWidget.addWidget(self.vnp)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.view_payment)

        self.setup()

    def setup(self):
        self.view_payment.clicked.connect(self.go_to_view_payment)
        self.view_not_payed.clicked.connect(self.go_to_view_not_payed)

    def go_to_view_payment(self):
        self.stackedWidget.setCurrentIndex(1)
        self.vp.populate_combos()
        self.vp.setup_table()
        self.vp.show_students_list()
        self.buttons(self.view_payment)

    def go_to_view_not_payed(self):
        self.stackedWidget.setCurrentIndex(2)
        self.vnp.populate_classes()
        self.buttons(self.view_not_payed)

    def buttons(self, button:QPushButton):
        self.view_payment.setStyleSheet("color: white")
        self.view_not_payed.setStyleSheet("color: white")

        button.setStyleSheet("color: green")
