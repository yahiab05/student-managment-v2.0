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
    
    
def income_added(where, id, amount , date, note) -> None:
    session = SessionLocal()

    if where == "bank":
        bank = Bank(income_id=id,income=amount, note=note)
        bank.date = bank.set_date(date)
        session.add(bank)
    else:
        caisse = Caisse(income_id=id, income=amount, note=note)
        caisse.date = caisse.set_date(date)
        session.add(caisse)

    session.commit()
    session.close()
    
def pydate_to_qdate(pydate) -> QDate:
    return QDate.fromString(pydate.strftime("%Y-%m-%d"), "yyyy-MM-dd")

@staticmethod
def expense_added(where, id, amount, date, note) -> None:
    session = SessionLocal()

    if where == "bank":
        bank = Bank(expense_id=id, expense=amount, note=note)
        bank.date = bank.set_date(date)
        session.add(bank)
    else:
        caisse = Caisse(expense_id=id, expense=amount, note=note)
        caisse.date = caisse.set_date(date) 
        session.add(caisse)

    session.commit()
    session.close()

def income_updated(where, id, amount):
    session = SessionLocal()

    if where == "bank":
        bank = session.query(Bank).filter(Bank.income_id == id).first()            
        bank.income = amount
    else:
        caisse = session.query(Caisse).filter(Caisse.income_id == id).first()            
        caisse.income = amount

    session.commit()
    session.close()


def expense_updated(where, id, amount) -> None:
    session = SessionLocal()

    if where == "bank":
        bank = session.query(Bank).filter(Bank.expense_id == id).first()            
        bank.expense = amount
    else:
        caisse = session.query(Caisse).filter(Caisse.expense_id == id).first()            
        caisse.expense = amount

    session.commit()
    session.close()

# delete if not needed
def get_next_auto_increment():
    session = SessionLocal()
    
    query = text(f"""
        SELECT AUTO_INCREMENT 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = :db_name AND TABLE_NAME = :table_name
    """)
    
    result = session.execute(query, {"db_name": "students1", "table_name": "entery"}).scalar()
    
    session.close()
    return result
    
# delete if not needed
def bank_or_caisse(where, identifier) -> int:
    session = SessionLocal()

    if where == "i":
        caisse = session.query(Caisse).filter(Caisse.income_id == identifier).first()

        if caisse is not None:
            return 0
        else:
            return 1
    else:
        caisse = session.query(Caisse).filter(Caisse.expense_id == identifier).first()

        if caisse is not None:
            return 0
        else:
            return 1
        

