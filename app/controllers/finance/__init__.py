from PyQt6.QtWidgets import QWidget, QPushButton

from app.controllers.finance.income import EnteryLogic
from app.controllers.finance.expenses import OutMoneyLogic
from app.controllers.finance.balance import BalanceLogic
from app.controllers.finance.transfer import TransferLogic

from app.ui.ui_forms import MoneyUI
from app.utils import load_gui, UiPath, buttons

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
        buttons(self, self.add_money, self.out_money, self.solde, self.transfer)
        
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
        buttons(self, self.add_money, self.out_money, self.solde, self.transfer)

    def expenses(self):
        self.stackedWidget.setCurrentIndex(1)
        self.o.setup_table()
        self.o.populate_combo()
        buttons(self, self.out_money, self.add_money, self.solde, self.transfer)

    def balance(self):
        self.stackedWidget.setCurrentIndex(2)
        self.s.setup_table()
        self.s.populate_combo()  
        buttons(self, self.solde, self.add_money, self.out_money, self.transfer)    

    def go_to_transfer(self):
        self.stackedWidget.setCurrentIndex(3)
        self.t.setup_table()
        buttons(self, self.transfer, self.add_money, self.out_money, self.solde)   

