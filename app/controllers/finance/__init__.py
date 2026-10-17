from PyQt6.QtWidgets import QWidget, QPushButton

from app.controllers.finance.income import EnteryLogic
from app.controllers.finance.expenses import OutMoneyLogic
from app.controllers.finance.balance import BalanceLogic
from app.controllers.finance.transfer import TransferLogic

from app.ui.ui_forms import MoneyUI
from app.utils import load_gui, UiPath

class MoneyPart(QWidget, MoneyUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        load_gui(UiPath.FINANCE, "money.ui", self)

        self.e = EnteryLogic(self)
        self.o = OutMoneyLogic(self)
        self.s = BalanceLogic(self)
        self.t = TransferLogic(self)

        self.stackedWidget.addWidget(self.e)
        self.stackedWidget.addWidget(self.o)
        self.stackedWidget.addWidget(self.s)
        self.stackedWidget.addWidget(self.t)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.add_money)


        self.setup()

    def setup(self):
        self.add_money.clicked.connect(self.income)
        self.out_money.clicked.connect(self.expenses)
        self.solde.clicked.connect(self.balance)
        self.transfer.clicked.connect(self.go_to_transfer)

    def income(self):
        self.stackedWidget.setCurrentIndex(0)
        self.e.setup_table()
        self.e.populate_combo()
        self.buttons(self.add_money)

    def expenses(self):
        self.stackedWidget.setCurrentIndex(1)
        self.o.setup_table()
        self.o.populate_combo()
        self.buttons(self.out_money)

    def balance(self):
        self.stackedWidget.setCurrentIndex(2)
        self.s.setup_table()
        self.s.populate_combo()  
        self.buttons(self.solde)    

    def go_to_transfer(self):
        self.stackedWidget.setCurrentIndex(3)
        self.t.setup_table()
        self.buttons(self.transfer)   

    def buttons(self, button:QPushButton):
        self.add_money.setStyleSheet("color: white")
        self.out_money.setStyleSheet("color: white")
        self.solde.setStyleSheet("color: white")
        self.transfer.setStyleSheet("color: white")

        button.setStyleSheet("color: green")

