from dataclasses import dataclass
from .base_schema import BaseDataClass
from datetime import datetime
from abc import ABC

@dataclass
class FinanceSchema(ABC, BaseDataClass):
    name: str
    price: float
    code: int
    way: str
    type:str
    #optional
    cheq_num: str=""
    note: str=""
    
@dataclass
class EntrySchema(FinanceSchema):
    bill_number: str

    num_inscrit: int=None
    payment_date: datetime=None
    addition_date: datetime=None
    classroom: str=None
        
@dataclass
class ExpensesSchema(FinanceSchema):
    bill_num: str
    date: datetime

@dataclass
class StorageSchema(BaseDataClass):
    date: datetime

    income_id: int=None
    expense_id: int=None
    income: float=None
    expense: float=None
    note: str=""    