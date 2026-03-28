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
    
    def validate(self):
        if not super().validate():
            return False
        if self.name is None or self.name == "":
            raise ValueError("الاسم مطلوب")
        if self.price is None or self.price == 0:
            raise ValueError("المبلغ مطلوب")
        if self.code is None or self.code == 0:
            raise ValueError("رقم النوع مطلوب")
        if self.way is None or self.way == "":
            raise ValueError("طريقة الدفع مطلوب")
        if self.type is None or self.type == "":
            raise ValueError("نوع مطلوب")
        return True
    
@dataclass
class EntrySchema(FinanceSchema):
    bill_number: str

    num_inscrit: int=None
    payment_date: datetime=None
    addition_date: datetime=None
    classroom: str=None
    
    def validate(self):
        if not super().validate():
            return False
        if self.bill_number is None or self.bill_number == "":
            raise ValueError("رقم الفاتورة مطلوب")
        return True
        
@dataclass
class ExpensesSchema(FinanceSchema):
    bill_num: str
    date: datetime
    
    def validate(self):
        if not super().validate():
            return False
        if self.bill_num is None or self.bill_num == "":
            raise ValueError("رقم الفاتورة مطلوب")
        if self.date is None:
            raise ValueError("تاريخ الفاتورة مطلوب")
        return True

@dataclass
class StorageSchema(BaseDataClass):
    date: datetime

    income_id: int=None
    expense_id: int=None
    income: float=None
    expense: float=None
    note: str=""    
    
    def validate(self):
        if not super().validate():
            return False
        if self.date is None:
            raise ValueError("تاريخ الفاتورة مطلوب")
        if self.income is None and self.income_id is not None:
            raise ValueError("الدخل مطلوب")
        if self.expense is None and self.expense_id is not None:
            raise ValueError("الصرف مطلوب")
        return True