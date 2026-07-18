from ..repo.models import Entery as IncomeModel, OutMoney as ExpenseModel
from .basic_operations import CRUD


class Income(CRUD):
    # Concrete child class for income records that uses the entery table.
    def __init__(self, session):
        super().__init__(session, IncomeModel)


class Expense(CRUD):
    # Concrete child class for expense records that uses the outmoney table.
    def __init__(self, session):
        super().__init__(session, ExpenseModel)
