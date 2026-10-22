from PyQt6.QtWidgets import QHeaderView, QMessageBox
from PyQt6.uic import loadUi
from os import path

from PyQt6.QtCore import QSettings

from enum import StrEnum, auto

def set_username(username: str) -> None:
    settings = QSettings("Dar Coran", "Gestion")
    settings.setValue("username", username)

def get_username() -> str:
    settings = QSettings("Dar Coran", "Gestion")
    return settings.value("username", "") if settings.value("username") is not None and not "" else "yahia"

def error(message: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setText(message)
    msg.exec()
    msg.show()
    
def info(message: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText(message)
    msg.exec()
    msg.show()
    
def get_selection_status_stylesheet(is_selected: bool) -> str:
    if is_selected:
        string = "background-color: green;"
        string += "border: 0px solid black;"
        string += "border-radius: 10px;"
        return string
    else:
        string = "background-color: red;"
        string += "border: 0px solid black;"
        string += "border-radius: 10px;"
        return string
    
def set_header_resize_mode(table_view, model):
    header = table_view.horizontalHeader()
    
    for column in range(model.columnCount()):
        header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
        
    
def get_student_list(search_text: str) -> list:
    from app.repo import get_session, Students

    session = get_session()

    try:
        pattern = f"%{search_text}%"

        return (
            session.query(Students.id, Students.name)
            .filter(Students.name.ilike(pattern))
            .order_by(Students.name.asc(), Students.id.asc())
            .all()
        )
    finally:
        session.close()
        
class Account(StrEnum):
    BANK = auto()
    CAISSE = auto()
    
    @property
    def opposite(self):
        if self == Account.BANK:
            return Account.CAISSE
        elif self == Account.CAISSE:
            return Account.BANK
    
class ReportType(StrEnum):
    PRINT = auto()
    EXCEL = auto()
    
class WorkingMode(StrEnum):
    ADD = auto()
    UPDATE = auto()
    
class UiPath(StrEnum):
    STUDENTS = "../ui/students/"
    CLASSES = "../ui/classes/"
    TEACHERS = "../ui/teacher/"
    PAYMENTS = "../ui/payment/"
    OTHERS = "../ui/others/"
    FINANCE = "../ui/finance/"
    FORMS= "../ui/forms/"
    LOGIN = MAIN = "../ui/"
    
def load_gui(prefix: UiPath="", ui_file: str="", widget=None) -> None:
    if widget is None:
        raise ValueError("Widget must be provided to load the UI.")
    if not ui_file:
        raise ValueError("UI file name must be provided.")
    ui_file_path = path.abspath(path.join(path.dirname(__file__), prefix, ui_file))
    loadUi(ui_file_path, widget)
    
def traceback_to_string(exc: Exception) -> str:
    import traceback
    return ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))