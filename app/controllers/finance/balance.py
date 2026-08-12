from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDate
from os import path

from app.repo.database import SessionLocal
from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.repo.schemas import SchemaFactory
from app.utils import error, get_username, get_combo_manager, ReportType, ComboName, WorkingMode
from app.ui.ui_forms import BalanceUI
from app.controllers.popup import create_popup_factory, PopupKind


class BalanceLogic(QWidget, BalanceUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = path.abspath("../../ui/finance/solde.ui")
        loadUi(ui_path, self)

        self.model = None
        self.combo_manager = get_combo_manager()
        self.manager = get_model(ModelName.BALANCE)
        self.income_manager = get_model(ModelName.INCOME)
        self.expenses_manager = get_model(ModelName.EXPENSES)

        self.setup_table()
        self.reset()
        self.populate_combo()
        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.show_table)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.BALANCE)

        self.tbl.setModel(self.model)

        self.set_totals()

        self.tbl.hideColumn(self.model.ID_COLUMN)
        
    def populate_combo(self):
        self.combo_manager.update_combo(self.way, ComboName.WAY_PAYMENT)

    def show_table(self):
        op = None if self.operatore.currentText() == "" else self.operatore.currentText()
        price = None if self.price_input.value() == 0 else self.price_input.value()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        way = None if self.way.currentText() == "" else self.way.currentText() 

        data = self.manager.get_balance(
            way_payment=way, 
            from_date=from_date, 
            to_date=to_date, 
            price=price, 
            operator=op
            )
        
        self.model.refresh(data)
        self.tbl.repaint()

    def set_totals(self):
        total_expenses, total_income, balance = self.expenses_manager.get_total(),
        self.income_manager.get_total(), self.manager.get_balance()
        
        self.total_out.setText(str(total_expenses))
        self.total_in.setText(str(total_income))
        self.solde.setText(str(balance))

    def reset(self):
        self.operatore.setCurrentIndex(-1)
        self.price_input.setValue(0)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())
        self.way.setCurrentIndex(-1)
        
    def export(self, output_channel: ReportType):
        data = self.model.get_current_data()
        total_income, total_expenses, balance = self.income_manager.get_total(), 
        
        self.expenses_manager.get_total(), self.manager.get_balance()
        
        self.manager.set_dynamic_metadata(
            total_income, total_expenses, balance, data)
        self.manager.export_data(
            report_type=output_channel, 
            parent=self
            )
