from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate
from sqlalchemy import text

from app.repo.models import SessionLocal, Students
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
    
def get_student_list(search_text: str) -> list[Students]:
    session = SessionLocal()

    try:
        pattern = f"%{search_text.strip()}%"

        return (
            session.query(Students.num_inscrit, Students.name)
            .filter(Students.name.ilike(pattern))
            .order_by(Students.name.asc(), Students.num_inscrit.asc())
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