from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6.QtCore import QDate

from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.repo.schemas import SchemaFactory
from app.utils import error, get_username, get_combo_manager, ReportType, Account, load_gui, UiPath
from app.ui.ui_forms import TransferUI

class TransferLogic(QWidget, TransferUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.FINANCE, "transfer.ui", self)

        self.model = None
        self.combo_manager = get_combo_manager()
        self.manager = get_model(ModelName.TRANSFER)
        self.income_manager = get_model(ModelName.INCOME)
        self.expenses_manager = get_model(ModelName.EXPENSES)

        self.setup_table()
        self.reset()
        self.setup()
        self.show_table()

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
        price = self.price.value() if self.price.value() > 0 else None
        
        filters = self.manager.get_filter(
            from_date=from_date,
            to_date=to_date,
            price=price,
            operator=op
        )

        data = self.manager.get_by_filter(filters)
        self.model.refresh(data)
        self.set_totals(
            price=price,
            operator=op,
            from_date=from_date,
            to_date=to_date
        )
        
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
        
    def totals_to_bank(self, price=None, operator=None, from_date=None, to_date=None):
        filters_to_bank = self.manager.get_filter(
            from_date=from_date,
            to_date=to_date,
            price=price if price else None,
            operator=operator if operator else None,
            destination=Account.BANK.value
        )
        total = self.manager.get_total(filters_to_bank)
        return total
    
    def totals_to_caisse(self, price=None, operator=None, from_date=None, to_date=None):
        filters_to_caisse = self.manager.get_filter(
            from_date=from_date,
            to_date=to_date,
            price=price if price else None,
            operator=operator if operator else None,
            destination=Account.CAISSE.value
        )
        total = self.manager.get_total(filters_to_caisse)
        return total
    
    def expense_income_totals(self, price=None, operator=None, from_date=None, to_date=None, in_bank=True):
        income_filters = self.income_manager.get_filter(
            addition_from_date=from_date,
            addition_to_date=to_date,
            price=price if price else None,
            operator=operator if operator else None,
            in_bank=in_bank  # Assuming you want to filter income that is in the bank
        )
        income_total = self.income_manager.get_total(income_filters)

        expense_filters = self.expenses_manager.get_filters(
            from_date=from_date,
            to_date=to_date,
            price=price if price else None,
            operator=operator if operator else None,
            in_bank=in_bank  # Assuming you want to filter expenses that are in the bank
        )
        expense_total = self.expenses_manager.get_total(expense_filters)
        return income_total, expense_total
    
    def totals_summary(self, price=None, operator=None, from_date=None, to_date=None):
        total_to_bank = self.totals_to_bank(price, operator, from_date, to_date)
        total_to_caisse = self.totals_to_caisse(price, operator, from_date, to_date)
        income_bank_total, expense_bank_total = self.expense_income_totals(price, operator, from_date, to_date)
        income_caisse_total, expense_caisse_total = self.expense_income_totals(price, operator, from_date, to_date, in_bank=False)
        
        summary = {
            "total_to_bank": total_to_bank,
            "total_to_caisse": total_to_caisse,
            "income_bank_total": income_bank_total,
            "expense_bank_total": expense_bank_total,
            "income_caisse_total": income_caisse_total,
            "expense_caisse_total": expense_caisse_total
        }
        return summary
    
    def set_totals(self, price=None, operator=None, from_date=None, to_date=None):
        summary = self.totals_summary(price, operator, from_date, to_date)
        total_transfered = summary["total_to_bank"] - summary["total_to_caisse"]
        total_in_bank = summary["income_bank_total"] - summary["expense_bank_total"] + total_transfered
        total_in_caisse = summary["income_caisse_total"] - summary["expense_caisse_total"] - total_transfered
        self.total_bank.setText(str(total_in_bank))
        self.total_caisse.setText(str(total_in_caisse))