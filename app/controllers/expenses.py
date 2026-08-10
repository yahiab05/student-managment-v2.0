from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate
from .help import HelpLogic, Printing
from os import path
from .database import SessionLocal
from .models import Entery, Settings, OutMoney, Caisse, Bank
from tables_model.money_tables import EnteryTableModel, OutMoneyTableModel, BalanceTableModel, CaisseTabelModel, BankTabelModel
from sqlalchemy import func

from ..view import TableType, create_table_model
from ..models import get_model
from ..repo.schemas import SchemaFactory
from ..utils import error, get_username, get_combo_manager, ReportType
from ..ui.ui_forms import OutMoneyUI


class OutMoneyLogic(QWidget, OutMoneyUI):
    def __init__(self, parent = None):
        super().__init__(parent)

        ui_path = path.abspath(path.join(path.dirname(__file__), "..", "ui", "finance", "out.ui"))
        loadUi(ui_path, self)

        self.identifier = None
        self.model = None
        self.manager = get_model("expenses")
        self.combo_manager = get_combo_manager()
        self.settings_manager = get_model("settings")

        self.reset()
        self.reset_filter()
        self.setup()
        self.populate_combo()
        self.setup_table()

    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.delete)
        self.tbl.doubleClicked.connect(self.select_out)
        self.search_btn.clicked.connect(self.show_out)
        self.reset_btn.clicked.connect(self.reset_filter)
        self.way.currentTextChanged.connect(self.cheq_num_on_off)
        self.type.currentTextChanged.connect(self.get_code)
        self.code_input.valueChanged.connect(self.get_type)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.OUT_MONEY)

        self.tbl.setModel(self.model)

        self.total.setText(str(self.model.total_price))
        self.tbl.hideColumn(self.model.ID_COLUMN)

    def control(self, action):
        name = self.name.currentText()
        bill_num = self.bill_num.text()
        date = self.date.date()
        types = self.type.currentText()
        way = self.way.currentText()
        cheq_num = self.nb_cheque.text()
        price = self.price.value()
        note = self.note.text()
        code = self.code_input.value()
        in_bank = self.bank_caisse.currentText()
        
        entity = SchemaFactory.OUT_MONEY(
            name=name,
            bill_num=bill_num,
            date=date,
            type=types,
            way=way,
            cheq_num=cheq_num,
            price=price,
            note=note,
            code=code,
            in_bank=in_bank,
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
            if action == "add":
                if self.unique(bill_num, date.toPyDate()):
                    error("هذا المصروف موجود")
                    return
                else:
                    self.manager.create(entity)
            else:
                self.manager.update(self.identifier, entity)
        except Exception as e:
            error("حدث خطأ")
        finally:
            self.reset()
            self.reset_filter()
            self.show_out()

    def delete(self):
        self.manager.delete(self.identifier)

    def reset(self):
        self.identifier = 0

        self.name.setCurrentIndex(-1)
        self.date.setDate(QDate.currentDate())
        self.type.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.price.setValue(0)
        self.note.setText("")
        self.bill_num.setText("")
        self.nb_cheque.setText("")
        self.code_input.setValue(0)

    def reset_filter(self):
        self.operatore.setCurrentIndex(-1)
        self.price_search.setValue(0)
        self.way_search.setCurrentIndex(-1)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())
        self.type_search.setCurrentIndex(-1)
        self.name_search.setCurrentIndex(-1)

    def show_out(self):
        name = None if self.name_search.currentText() == "" else self.name_search.currentText()
        way = None if self.way_search.currentText() == "" else self.way_search.currentText()
        type = None if self.type_search.currentText() == "" else self.type_search.currentText()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        price = None if self.price_search.value() == 0 else self.price_search.value()
        operator = None if self.operatore.currentText() == "" else self.operatore.currentText()
        code = None if self.code_input.value() == 0 else self.code_input.value()

        filters = self.manager.get_filters(
            name=name,
            way=way,
            type=type,
            from_date=from_date,
            to_date=to_date,
            price=price,
            operator=operator,
            code=code
        )
        data = self.manager.get_by_filter(filters)
        self.model.refresh(data)

        self.total.setText(str(self.model.total_price))

    def populate_combo(self):
        self.combo_manager.update_combo(self.name, "fr")
        self.combo_manager.update_combo(self.types, "expenses")
        self.combo_manager.update_combo(self.way, "way payment")
        self.combo_manager.update_combo(self.name_search, "fr")
        self.combo_manager.update_combo(self.type_search, "expenses")
        self.combo_manager.update_combo(self.way_search, "way payment")

    def select_out(self):
        row = self.tbl.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد المصروف")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)

        self.tbl.clearSelection()
        self.populate()

    def populate(self):
        out = self.manager.get_by_id(self.identifier)
        if out is not None:
            self.name.setCurrentText(out.name)
            self.date.setDate(out.get_date())
            self.type.setCurrentText(out.type)
            self.way.setCurrentText(out.way)
            self.price.setValue(out.price)
            self.note.setText(out.note)
            self.bill_num.setText(str(out.bill_num))
            self.nb_cheque.setText(str(out.cheq_num))
            self.code_input.setValue(out.code)
            self.bank_caisse.setCurrentIndex(HelpLogic.bank_or_caisse("e", self.identifier))

    def unique(self, bill_num, date):
        filters = self.manager.get_filters(bill_num=bill_num, from_date=date, to_date=date)
        return self.manager.exists(filters)
    
    def cheq_num_on_off(self):
        if self.way.currentText() == "صك":
            self.nb_cheque.setEnabled(True)
        else:    
            self.nb_cheque.setEnabled(False)

    def get_code(self):
        code = self.settings_manager.get_code(
            income=None, 
            expense=self.type.currentText()
            )
        self.code.setValue(code if code is not None else 0)

    def get_type(self):
        expense = self.settings_manager.get_type(
            income_code=None,
            expense_code=self.code_input.value()
            )
        self.type.setCurrentText(expense if expense is not None else "")

    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        total = ...
        self.manager.set_dynamic_metadata(
            total_price=total, 
            data_to_export=data_to_export
            )
        
        self.manager.export_data(report_type=output_channel, parent=self)