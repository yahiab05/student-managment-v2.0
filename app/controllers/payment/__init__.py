from PyQt6.QtWidgets import QWidget

from app.controllers.payment.payments import ViewPayment
from app.controllers.payment.not_payed_view import ViewNotPayedLogic

from app.ui.ui_forms import PaymentPartUI
from app.utils import load_gui, UiPath, buttons

class PaymentPart(QWidget, PaymentPartUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        load_gui(UiPath.PAYMENTS, "payment_part.ui", self)

        self.vp = ViewPayment()
        self.vnp = ViewNotPayedLogic()

        self.stackedWidget.addWidget(self.vp)
        self.stackedWidget.addWidget(self.vnp)

        self.stackedWidget.setCurrentIndex(0)
        buttons(self, self.view_payment, self.view_not_payed)

        self.setup()

    def setup(self):
        self.view_payment.clicked.connect(self.go_to_view_payment)
        self.view_not_payed.clicked.connect(self.go_to_view_not_payed)

    def go_to_view_payment(self):
        self.stackedWidget.setCurrentIndex(0)
        self.vp.populate_combos()
        self.vp.setup_table()
        self.vp.show_students_list()
        buttons(self, self.view_payment, self.view_not_payed)

    def go_to_view_not_payed(self):
        self.stackedWidget.setCurrentIndex(1)
        self.vnp.populate_classes()
        buttons(self, self.view_not_payed, self.view_payment)
