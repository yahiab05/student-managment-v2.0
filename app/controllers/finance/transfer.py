from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6.QtCore import QDate
from os import path

from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.repo.schemas import SchemaFactory
from app.utils import error, get_username, get_combo_manager, ReportType, ComboName, Account
from app.ui.ui_forms import TransferUI

class TransferLogic(QWidget, TransferUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = path.abspath("../../ui/finance/transfer.ui")
        loadUi(ui_path, self)

        self.model = None
        self.combo_manager = get_combo_manager()
        self.manager = get_model(ModelName.TRANSFER)

        self.setup_table()
        self.reset()
        self.setup()

    def setup(self):
        self.to_bank_btn.clicked.connect(lambda: self.transfer_security(Account.BANK))
        self.to_caisse_btn.clicked.connect(lambda: self.transfer_security(Account.CAISSE))
        self.search_btn.clicked.connect(self.show_table)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.TRANSFER)

        self.table.setModel(self.model)
        self.table.hideColumn(self.model.ID_COLUMN)

    def transfer_security(self, account: Account):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا الدخل ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.transfer_order(account)
        else:
            self.reset()

    def transfer_order(self, account: Account):
        # Placeholder for transfer order logic
        date = self.date.date().toPyDate()
        amount = self.price.value()
        note = self.note.text()
        
        entity = SchemaFactory.TRANSFER(
            price=amount,
            destination=account.value,
            origin=account.opposite.value,
            date=date,
            note=note,
            user=get_username()
        )
        
        try:
            if not entity.validate():
                error("الرجاء ملء جميع الحقول")
                return
        except ValueError as e:
            error(str(e))
            return
        try:
            self.manager.create(entity)
            self.reset()
        except Exception as e:
            error(str(e))

    def show_table(self):
        op = self.operatore.currentText() if self.operatore.currentText() else None
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        
        filters = self.manager.get_filter(
            from_date=from_date,
            to_date=to_date,
            price=self.price.value() if self.price.value() > 0 else None,
            operator=op if op else None
        )

        data = self.manager.get_by_filter(filters)
        self.model.refresh(data)
        
    def reset(self):
        self.date.setDate(QDate.currentDate())
        self.price.setValue(0)
        self.note.clear()
        self.operatore.setCurrentIndex(0)
        self.du.setDate(QDate.currentDate())
        self.to.setDate(QDate.currentDate())

    def export(self, report_type: ReportType):
        data_to_export = self.model.get_current_data()
        total_price = sum(row.price for row in data_to_export)  # Assuming price is in the second column
        
        self.manager.set_dynamic_metadata(total_price, data_to_export)
        
        self.manager.export_data(report_type=report_type, parent=self)