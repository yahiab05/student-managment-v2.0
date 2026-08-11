from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget
from os import path
from typing import Protocol
from app.utils import get_combo_manager, ComboName
from models import get_model, ModelName

from app.ui.ui_forms import (
    ClassesFormUI,
    ExpensesFormUI,
    IncomeFormUI,
    SettingFormUI,
    SettingWithCodeFormUI,
    StudentFormUI,
    TeacherFormUI,
)

class FormProtocol(Protocol):
    def __init__(self, parent=None): ...

    def get_data(self) -> dict: ...
        
    def repopulate_fields(self, data: dict) -> None: ...

class FormWithCombosToPopulateProtocol(FormProtocol, Protocol):
    def populate_combos(self) -> None: ...

def _load_form_ui(widget: QWidget, *ui_parts: str) -> None:
    ui_path = path.abspath(path.join(path.dirname(__file__), "..", "..", "ui", *ui_parts))
    loadUi(ui_path, widget)
    

class StudentForm(QWidget, StudentFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "student_form.ui")
        
    def get_data(self):
        return {
            "name": self.name.text(),
            "parent": self.parent_ent.text(),
            "num_tel": self.num_tel.text(),
            "num_tel_2": self.num_tel_2.text(),
            "cin": self.cin.text(),
            "birthday": self.birthday.date().toPyDate(),
            "activity": self.activity.currentText(),
            "excused": self.excused.currentText(),
            "date_inscrit": self.date_inscrit.date().toPyDate(),
            "note":self.note.text(),
            "gender": self.gender.currentText()
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.parent_ent.setText(data.get("parent", ""))
        self.num_tel.setText(data.get("num_tel", ""))
        self.num_tel_2.setText(data.get("num_tel_2", ""))
        self.cin.setText(data.get("cin", ""))
        self.birthday.setDate(data.get("birthday", self.birthday.date()))
        self.activity.setCurrentText(data.get("activity", ""))
        self.excused.setCurrentText(data.get("excused", ""))
        self.date_inscrit.setDate(data.get("date_inscrit", self.date_inscrit.date()))
        self.note.setText(data.get("note", ""))
        self.gender.setCurrentText(data.get("gender", ""))


class TeacherForm(QWidget, TeacherFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "teacher_form.ui")

    def get_data(self):
        return {
            "name": self.name.text(),
            "date_inscrit": self.date_inscrit.date().toPyDate(),
            "birthday": self.birthday.date().toPyDate(),
            "phone": self.phone.text(),
            "phone_2": self.phone_2.text(),
            "note": self.note.text(),
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.date_inscrit.setDate(data.get("date_inscrit", self.date_inscrit.date()))
        self.birthday.setDate(data.get("birthday", self.birthday.date()))
        self.phone.setText(data.get("phone", ""))
        self.phone_2.setText(data.get("phone_2", ""))
        self.note.setText(data.get("note", ""))


class ClassesForm(QWidget, ClassesFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "classes_form.ui")
        
        self.combo_manager = get_combo_manager()

    def get_data(self):
        return {
            "name": self.name.text(),
            "way": self.way.currentText(),
            "price": self.price.text(),
            "note": self.note.text(),
            "teacher": self.teacher.currentText(),
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.way.setCurrentText(data.get("way", ""))
        self.price.setText(data.get("price", ""))
        self.note.setText(data.get("note", ""))
        self.teacher.setCurrentText(data.get("teacher", ""))
        
    def populate_combos(self) -> None:
        self.combo_manager.update_combo(self.teacher, ComboName.TEACHER)
        self.combo_manager.update_combo(self.way, ComboName.WAY_TEACHING)


class ExpensesForm(QWidget, ExpensesFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "expenses_form.ui")
        
        self.combo_manager = get_combo_manager()
        self.settings_manager = get_model(ModelName.SETTINGS)

    def get_data(self):
        return {
            "name": self.name.currentText(),
            "bill_num": self.bill_num.text(),
            "way": self.way.currentText(),
            "code_input": self.code_input.value(),
            "date": self.date.date().toPyDate(),
            "type": self.type.currentText(),
            "bank_caisse": self.bank_caisse.currentText(),
            "note": self.note.text(),
            "nb_cheque": self.nb_cheque.text(),
            "price": self.price.value(),
        }

    def repopulate_fields(self, data: dict) -> None:
        self.name.setCurrentText(data.get("name", ""))
        self.bill_num.setText(data.get("bill_num", ""))
        self.way.setCurrentText(data.get("way", ""))
        self.code_input.setValue(data.get("code_input", 0))
        self.date.setDate(data.get("date", self.date.date()))
        self.type.setCurrentText(data.get("type", ""))
        self.bank_caisse.setCurrentText(data.get("bank_caisse", ""))
        self.note.setText(data.get("note", ""))
        self.nb_cheque.setText(data.get("nb_cheque", ""))
        self.price.setValue(data.get("price", 0.0))
        
    def populate_combos(self) -> None:
        self.combo_manager.update_combo(self.name, ComboName.FR)
        self.combo_manager.update_combo(self.way, ComboName.WAY_PAYMENT)
        self.combo_manager.update_combo(self.type, ComboName.EXPENSES)  
        
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
        self.code_input.setValue(code if code is not None else 0)

    def get_type(self):
        expense = self.settings_manager.get_type(
            income_code=None,
            expense_code=self.code_input.value()
            )
        self.type.setCurrentText(expense if expense is not None else "")

class IncomeForm(QWidget, IncomeFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "income_from.ui")
        
        self.combo_manager = get_combo_manager()
        self.setting_manager

    def get_data(self):
        return {
            "name": self.name.text(),
            "date": self.date.date().toPyDate(),
            "code_input": self.code_input.value(),
            "type": self.type.currentText(),
            "way": self.way.currentText(),
            "bill_number": self.bill_number.text(),
            "nb_cheque": self.nb_cheque.text(),
            "bank_caisse": self.bank_caisse.currentText(),
            "price": self.price.value(),
            "note": self.note.text(),
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.date.setDate(data.get("date", self.date.date()))
        self.code_input.setValue(data.get("code_input", 0))
        self.type.setCurrentText(data.get("type", ""))
        self.way.setCurrentText(data.get("way", ""))
        self.bill_number.setText(data.get("bill_number", ""))
        self.nb_cheque.setText(data.get("nb_cheque", ""))
        self.bank_caisse.setCurrentText(data.get("bank_caisse", ""))
        self.price.setValue(data.get("price", 0.0))
        self.note.setText(data.get("note", ""))
        
    def populate_combos(self) -> None:
        self.combo_manager.update_combo(self.type, ComboName.INCOME)
        self.combo_manager.update_combo(self.way, ComboName.WAY_PAYMENT)
        
class PaymentForm(QWidget, SettingFormUI):
    raise NotImplementedError("PaymentForm is not implemented yet.")

