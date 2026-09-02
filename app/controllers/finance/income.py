from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDate

from app.repo.schemas import SchemaFactory

from app.utils import (
    error, 
    get_username, 
    get_combo_manager, 
    ReportType, 
    ComboName,
    WorkingMode,
    load_gui,
    UiPath,
    get_selection_status_stylesheet
    )

from app.view import TableType, create_table_model
from app.models import ModelName, get_model
from app.controllers.popup import create_popup_factory, PopupKind
from app.ui.ui_forms import EnteryMoneyUI

class EnteryLogic(QWidget, EnteryMoneyUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.FINANCE, "entery.ui", self)

        self.identifier = None
        self.model = None
        self.manager = get_model(ModelName.INCOME)
        self.combo_manager = get_combo_manager
        self.settings_manager = get_model(ModelName.SETTINGS)
        
        self.populate_combo()
        self.reset_filter()
        self.setup_table()
        self.setup()
        self.deselection()

    def setup(self):
        self.add_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.aquire_data(WorkingMode.UPDATE))
        self.reset_btn.clicked.connect(self.reset_filter)
        self.search_btn.clicked.connect(self.show_entery)
        self.tbl.doubleClicked.connect(self.select)
        self.delete_btn.clicked.connect(self.delete_income) 
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):

        self.model = create_table_model(TableType.INCOME)

        self.tbl.setModel(self.model)

        self.tbl.hideColumn(self.model.ID_COLUMN)   
    
    def selection(self, identifier):
        self.identifier = identifier
        self.select_info.setStyleSheet(get_selection_status_stylesheet(True))
        
    def deselection(self):
        self.identifier = None
        self.select_info.setStyleSheet(get_selection_status_stylesheet(False))
        
    def aquire_data(self, action:WorkingMode):
        dialog = create_popup_factory(
            kind=PopupKind.INCOME,
            title="إضافة دخل" if action == WorkingMode.ADD else "تعديل دخل",
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
        in_bank = True if data["in_bank"] == "البنك" else False
        entity = SchemaFactory.INCOME(  
                name=data["name"],
                addition_date=data["date"],
                type=data["type"],
                way=data["way"],
                price=data["price"],
                note=data["note"],
                bill_number=data["bill_number"],
                cheq_num=data["cheq_num"],
                code=data["code_input"],
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

        if action == WorkingMode.ADD:
            self.manager.create(entity)
        else:
            self.manager.update(self.identifier, entity)
            self.deselection()
        self.show_entery()

    def select(self, index=None):
        row = index.row()
        if row is None:
            error("يرجى تحديد الدخل")
            return
        
        row_index = row   

        identifier = self.model.data(self.model.index(row_index, 0), role=0)
        types = self.model.data(self.model.index(row_index, 5), role=0)  

        self.tbl.clearSelection()

        if types == "تسجيل":
            self.identifier = 0
            error("لا يمكن التحديث")
            return
        
        self.selection(identifier)
        
    def delete_income(self):
        if self.identifier is None:
            error("يرجى تحديد الدخل")
            return
        try:
            self.manager.sup_security(widget=self, id=self.identifier, text="متأكد من حذف هذا الدخل ؟")
            self.show_entery()
            self.deselection()
        except Exception as e:
            error("حدث خطأ", e)

    def reset_filter(self):
        self.operatore.setCurrentIndex(-1)
        self.price_search.setValue(0)
        self.way_search.setCurrentIndex(-1)
        self.type_search.setCurrentIndex(-1)
        self.to.setDate(QDate.currentDate())
        self.du.setDate(QDate(2000, 1, 1))
        self.code.setValue(0)
        self.name_search.setText("")

    def show_entery(self):
        name = None if self.name_search.text() == "" else self.name_search.text()
        way = None if self.way_search.currentText() == "" else self.way_search.currentText()
        type = None if self.type_search.currentText() == "" else self.type_search.currentText()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        price = None if self.price_search.value() == 0 else self.price_search.value()
        operator = None if self.operatore.currentText() == "" else self.operatore.currentText()
        code = None if self.code.value() == 0 else self.code.value()

        filters = self.manager.get_filter(
            name=name,
            way=way,
            type=type,
            addition_from_date=from_date,
            addition_to_date=to_date,
            price=price,
            operator=operator,
            code=code
        )
        
        data = self.manager.get_by_filter(filters)
        
        self.model.refresh(data)
        self.tbl.repaint()

        self.total.setText(str(self.manager.get_total(filters)))

    def populate_combo(self):
        self.combo_manager.update_combo(self.type_search, ComboName.INCOME)
        self.combo_manager.update_combo(self.way_search, ComboName.WAY_PAYMENT)

    def get_code(self):
        expense_type = self.settings_manager.get_code(income=self.type_search.currentText(), expense=None)
        if expense_type is None:
            self.code.setValue(0)
        else:
            self.code.setValue(expense_type)
            
    def get_type(self):
        code = self.settings_manager.get_type(income_code=self.code.value(), expense_code=None)
        if code is None:
            self.type_search.setCurrentIndex(-1)
        else:
            self.type_search.setCurrentText(code[0])

    def export(self, output_channel: ReportType):
        data_to_export = self.model.get_current_data()
        total_price = self.get_total(data_to_export)
        self.manager.set_dynamic_metadata(total_price, data_to_export)

        self.manager.export_data(
            report_type=output_channel, 
            parent=self)
        
    def get_total(self, data):
        total = 0
        for item in data:
            total += item.price
        return total
