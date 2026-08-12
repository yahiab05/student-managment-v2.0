from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDate
from os import path

from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.repo.schemas import SchemaFactory
from app.utils import error, get_username, get_combo_manager, ReportType, ComboName, WorkingMode
from app.ui.ui_forms import OutMoneyUI
from app.controllers.popup import create_popup_factory, PopupKind


class OutMoneyLogic(QWidget, OutMoneyUI):
    def __init__(self, parent = None):
        super().__init__(parent)

        ui_path = path.abspath(path.join(path.dirname(__file__), "..", "ui", "finance", "out.ui"))
        loadUi(ui_path, self)

        self.identifier = None
        self.model = None
        self.manager = get_model(ModelName.EXPENSES)
        self.combo_manager = get_combo_manager()
        self.settings_manager = get_model(ModelName.SETTINGS)

        self.reset_filter()
        self.setup()
        self.populate_combo()
        self.setup_table()

    def setup(self):
        self.add_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete)
        self.tbl.doubleClicked.connect(self.select_out)
        self.search_btn.clicked.connect(self.show_out)
        self.reset_btn.clicked.connect(self.reset_filter)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.OUT_MONEY)

        self.tbl.setModel(self.model)

        self.total.setText(str(self.model.total_price))
        self.tbl.hideColumn(self.model.ID_COLUMN)
        
    def aquire_data(self, action: WorkingMode):
        dialog = create_popup_factory(
            kind=PopupKind.EXPENSES, 
            title="إضافة مصروف" if action == WorkingMode.ADD else "تعديل مصروف", 
            parent=self
        )
        if action == WorkingMode.UPDATE:
            data = self.manager.get_by_id(self.identifier)
            dialog.content.repopulate_fields(data.__dict__)
        
        def on_confirm():
            data = dialog.content.get_data()
            self.control(action, data)
            
        dialog.confirmed.connect(on_confirm)
        dialog.show()
        
    def control(self, action, data):
        entity = SchemaFactory.EXPENSES(
            name=data["name"],
            bill_num=data["bill_num"],
            date=data["date"],
            type=data["type"],
            way=data["way"],
            cheq_num=data["cheq_num"],
            price=data["price"],
            note=data["note"],
            code=data["code"],
            in_bank=data["in_bank"],
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
            if action == WorkingMode.ADD:
                if self.unique(data["bill_num"], data["date"]):
                    error("هذا المصروف موجود")
                    return
                else:
                    self.manager.create(entity)
            else:
                self.manager.update(self.identifier, entity)
        except Exception as e:
            error("حدث خطأ")
        finally:
            self.reset_filter()
            self.show_out()

    def delete(self):
        self.manager.delete(self.identifier)

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
        code = None if self.code.value() == 0 else self.code.value()

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
        self.combo_manager.update_combo(self.name_search, ComboName.FR)
        self.combo_manager.update_combo(self.type_search, ComboName.EXPENSES)
        self.combo_manager.update_combo(self.way_search, ComboName.WAY_PAYMENT)

    def select_out(self):
        row = self.tbl.selectionModel().selectedRows()
        if not row:
            error("يرجى تحديد المصروف")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)

        self.tbl.clearSelection()
        self.aquire_data("update")
        
        
    def unique(self, bill_num, date):
        filters = self.manager.get_filters(bill_num=bill_num, from_date=date, to_date=date)
        return self.manager.exists(filters)

    def get_code(self):
        code = self.settings_manager.get_code(
            income=None, 
            expense=self.type_search.currentText()
            )
        self.code.setValue(code if code is not None else 0)

    def get_type(self):
        expense = self.settings_manager.get_type(
            income_code=None,
            expense_code=self.code.value()
            )
        self.type_search.setCurrentText(expense if expense is not None else "")

    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        total = ...
        self.manager.set_dynamic_metadata(
            total_price=total, 
            data_to_export=data_to_export
            )
        
        self.manager.export_data(report_type=output_channel, parent=self)