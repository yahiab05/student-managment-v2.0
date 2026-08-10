from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget
from os import path
from typing import Protocol

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


class ClassesForm(QWidget, ClassesFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "classes_form.ui")

    def get_data(self):
        return {
            "name": self.name.text(),
            "way": self.way.currentText(),
            "price": self.price.text(),
            "note": self.note.text(),
            "teacher": self.teacher.currentText(),
        }


class ExpensesForm(QWidget, ExpensesFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "expenses_form.ui")

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


class IncomeForm(QWidget, IncomeFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "income_from.ui")

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


class SettingForm(QWidget, SettingFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "setting_form.ui")

    def get_data(self):
        return {
            "entery": self.entery.text(),
        }


class SettingWithCodeForm(QWidget, SettingWithCodeFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        _load_form_ui(self, "forms", "setting_with_code_form.ui")

    def get_data(self):
        return {
            "entery": self.entery.text(),
            "code": self.code.value(),
        }
        

