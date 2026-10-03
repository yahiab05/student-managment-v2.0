from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from sqlalchemy.exc import IntegrityError
from app.repo.schemas import SchemaFactory
from app.utils import get_username, error, get_combo_manager, WorkingMode, ComboName, load_gui, UiPath
from app.models import ModelName, get_model
from app.ui.ui_forms import SettingWithCodeFormUI, SettingFormUI, SettingsUI

class BaseSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.manager = get_model(ModelName.SETTINGS)
        self.combo_manager = get_combo_manager
        
    """Out section"""
    def setup(self):
        self.reset_btn.clicked.connect(self.reset_enteries)
        self.add_btn.clicked.connect(lambda: self.control(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.control(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete)
        self.list.doubleClicked.connect(self.select_row)
        self.entery.textChanged.connect(lambda: self.show_data(self.entery.text()))

    def control(self, action):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def delete(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def check_used(self, code):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def reset_enteries(self):
        #self.code.setValue(0)
        self.entery.setText("")

        self.show_data()

    def select_row(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def show_data(self, name=None):
        raise NotImplementedError("This method should be implemented in subclasses.")
    
class SettingsWithCode(BaseSettings, SettingWithCodeFormUI):
    def __init__(self, is_income, parent=None):
        BaseSettings.__init__(self, parent=parent)
        
        load_gui(UiPath.FORMS, "setting_with_code_form.ui", self)
        
        self.identifier = None
        self.income = is_income
        
        self.setup()
        self.list.setColumnHidden(0, True)

    def control(self, action):
        name = self.entery.text()
        code = self.code.text()
        username = get_username()
        
        if self.income:
            entity = SchemaFactory.SETTINGS(entery=name, entery_code=int(code), user=username)
        else:
            entity = SchemaFactory.SETTINGS(out_money=name, out_code=int(code), user=username)
        
        if not entity.validate():
            error("Verifier les données")
            return
        if action == WorkingMode.ADD:
            try:
                self.manager.create(entity)
            except IntegrityError:
                error("Ce code est déjà utilisé. Veuillez en choisir un autre.")
                return
        else:
            try:
                self.manager.update(self.identifier, entity)
            except IntegrityError:
                error("Ce code est déjà utilisé. Veuillez en choisir un autre.")
                return

        self.reset_enteries()
        self.identifier = None
        self.show_data()
        self.combo_manager.update_cache_from_db(ComboName.INCOME if self.income else ComboName.EXPENSES)
        
    def delete(self):
        try:
            self.manager.sup_security(widget=self, id=self.identifier, text="متأكد من حذف هذا النوع ؟")
        except IntegrityError:
            error("لا يمكن الحذف لأنه يتم إستعماله")
        finally:
            self.reset_enteries()
            self.identifier = None

    def select_row(self, index):
        row = index.row()
        print("Selected row index:", row)
        self.identifier = int(self.list.item(row, 0).text())
        print("Selected identifier:", self.identifier)
        print("Selected entery:", self.list.item(row, 1).text())
        print("Selected entery:", self.list.item(row, 2))
        self.code.setValue(int(self.list.item(row, 2).text()))
        self.entery.setText(self.list.item(row, 1).text())
        
        
    def show_data(self, filters):
        data = self.manager.get_by_filter(filters)
        self.list.setRowCount(len(data))
        
        if len(data) > 0:
            for i, class_obj in enumerate(data):
                self.list.setItem(i, 0, QTableWidgetItem(str(class_obj.id)))
                self.list.setItem(i, 1, QTableWidgetItem(
                    str(class_obj.out_money) if not self.income else str(class_obj.entery)
                    ))
                
                self.list.setItem(i, 2, QTableWidgetItem(
                    str(class_obj.out_code) if not self.income else str(class_obj.entery_code)
                    ))

        self.nb.setText(str(len(data)))    
        
    def reset_enteries(self):
        self.code.setValue(0)
        return super().reset_enteries()
    
class IncomeSettings(SettingsWithCode):
    def __init__(self, parent=None):
        super().__init__(is_income=True, parent=parent)
        
        self.title.setText("Type de revenu")
        
        self.show_data()
        
    def check_used(self, code):
        model = get_model(ModelName.INCOME)
        return model.check_used(code)
    
    def show_data(self, name=""):
        filters = self.manager.get_filter(entery=name)
        super().show_data(filters)

class ExpenseSettings(SettingsWithCode):
    def __init__(self, parent=None):
        super().__init__(is_income=False, parent=parent)
        
        self.title.setText("Type de dépense")
        
        self.show_data()
    def check_used(self, code):
        model = get_model(ModelName.EXPENSE)
        return model.check_used(code)
    
    def show_data(self, name=""):
        filters = self.manager.get_filter(out_money=name)
        super().show_data(filters)

class SettingsWithoutCode(BaseSettings, SettingFormUI):
    def __init__(self, setting: ComboName, parent=None):
        BaseSettings.__init__(self, parent=parent)

        load_gui(UiPath.FORMS, "setting_form.ui", self)
        
        self.setting = setting
        
        self.item = None

        self.setup()
        
    def control(self, action:WorkingMode):
        name = self.entery.text()
        username = get_username()
        
        if self.setting == ComboName.WAY_TEACHING:
            entity = SchemaFactory.SETTINGS(way_teaching=name, user=username)
        elif self.setting == ComboName.WAY_PAYMENT:
            entity = SchemaFactory.SETTINGS(way_payment=name, user=username)
        elif self.setting == ComboName.FR:
            entity = SchemaFactory.SETTINGS(fr=name, user=username)
        else:
            error("Invalid setting type")
            return

        if not entity.validate():
            error("Verifier les données")
            return
        if action == WorkingMode.ADD:
            try:
                self.manager.create(entity)
            except IntegrityError:
                error("Ce code est déjà utilisé. Veuillez en choisir un autre.")
                return
        else:
            try:
                filter = self.get_appropriate_filter(self.item)
                self.manager.update_by_filter(filter, entity)
            except IntegrityError:
                error("Ce code est déjà utilisé. Veuillez en choisir un autre.")
                return
            
        self.reset_enteries()
        self.identifier = None
        self.show_data()
        self.combo_manager.update_cache_from_db(self.setting)
        
    def delete(self):
        name = self.entery.text()
        try:
            filter = self.get_appropriate_filter(name)
            self.manager.sup_security(widget=self, text= "متأكد من حذف هذا النوع ؟", filter=filter)
        except IntegrityError as e:
            error("لا يمكن الحذف لأنه يتم إستعماله")
        finally:
            self.reset_enteries()
            self.identifier = None
            self.combo_manager.update_cache_from_db(self.setting)
                
    def get_appropriate_filter(self, name):
        if self.setting == ComboName.WAY_TEACHING:
            return self.manager.get_filter(way_teaching=name)
        elif self.setting == ComboName.WAY_PAYMENT:
            return self.manager.get_filter(way_payment=name)
        elif self.setting == ComboName.FR:
            return self.manager.get_filter(fr=name)
        else:
            raise ValueError("Invalid setting type")
        
    def select_row(self):
        row = self.list.currentItem().text()
        self.entery.setText(row)
        self.item = row 
        
    def show_data(self, filters: list=[]):
        data = self.manager.get_by_filter(filters)
        self.list.clear()
        
        if len(data) > 0:
            for i, class_obj in enumerate(data):
                if self.setting == ComboName.WAY_TEACHING:
                    self.list.addItem(class_obj.way_teaching)
                elif self.setting == ComboName.WAY_PAYMENT:
                    self.list.addItem(class_obj.way_payment)
                elif self.setting == ComboName.FR:
                    self.list.addItem(class_obj.fr)
                    
        self.nb.setText(str(len(data))) 

class WaySettings(SettingsWithoutCode):
    def __init__(self, parent=None):
        super().__init__(setting=ComboName.WAY_TEACHING, parent=parent)
        
        self.title.setText("Méthode d'enseignement")
        
        self.show_data()

    def check_used(self, way):
        model = get_model(ModelName.CLASSES)
        filters = model.get_filters(way_teaching=way)
        return model.exists(filters)

    def show_data(self, name=""):
        filters = self.manager.get_filter(way_teaching=name)
        print("specific filters: ", filters)
        super().show_data(filters)

class PaymentSettings(SettingsWithoutCode):
    def __init__(self, parent=None):
        super().__init__(setting=ComboName.WAY_PAYMENT, parent=parent)
        
        self.title.setText("Méthode de paiement")
        
        super().show_data()

    def check_used(self, name):
        return self.used_per_model(ModelName.INCOME, name) \
        or self.used_per_model(ModelName.EXPENSE, name)

    @staticmethod
    def used_per_model(model_name: ModelName, name: str):
        model = get_model(model_name)
        filters = model.get_filter(way_payment=name)
        return model.exists(filters)

    def show_data(self, name=""):
        filters = self.manager.get_filter(way_payment=name)
        super().show_data(filters)

class FournisseurSettings(SettingsWithoutCode):
    def __init__(self, parent=None):
        super().__init__(setting=ComboName.FR, parent=parent)

        self.show_data()
        self.title.setText("Fournisseur")

    def fournisseur_check_used(self, name):
        model = get_model(ModelName.EXPENSES)
        filters = model.get_filters(name=name)
        return model.exists(filters)

    def show_data(self, name=""):
        filters = self.manager.get_filter(fr=name)
        super().show_data(filters)