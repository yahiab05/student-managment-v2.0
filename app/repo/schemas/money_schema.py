from dataclasses import dataclass
from app.repo.schemas.base_schema import BaseDataClass
from datetime import datetime
from app.utils import Account

@dataclass(kw_only=True)
class FinanceSchema(BaseDataClass):
    name: str
    price: float
    code: int
    way: str
    type:str
    in_bank: bool
    bill_number: str
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
        if self.bill_number is None or self.bill_number == "":
            raise ValueError("رقم الفاتورة مطلوب")
        return True
    
@dataclass
class EntrySchema(FinanceSchema):
    num_inscrit: int=None
    payment_date: datetime=None
    addition_date: datetime=None
    classroom: str=None
    
    def validate(self):
        if not super().validate():
            return False
        return True
        
@dataclass
class ExpensesSchema(FinanceSchema):
    date: datetime
    
    def validate(self):
        if not super().validate():
            return False
        if self.bill_number is None or self.bill_number == "":
            raise ValueError("رقم الفاتورة مطلوب")
        if self.date is None:
            raise ValueError("تاريخ الفاتورة مطلوب")
        return True

@dataclass
class TransferSchema(BaseDataClass):
    price: float
    origin: Account
    destination: Account
    date: datetime
    user: str
    #optional
    note: str=""
    
    def validate(self):
        if not super().validate():
            return False
        if self.price is None or self.price == 0:
            raise ValueError("المبلغ مطلوب")
        if self.origin is None or self.origin == "":
            raise ValueError("الحساب الأصلي مطلوب")
        if self.destination is None or self.destination == "":
            raise ValueError("الحساب الوجهة مطلوب")
        if self.date is None:
            raise ValueError("تاريخ التحويل مطلوب")
        if self.destination == self.origin:
            raise ValueError("الحساب الوجهة لا يمكن أن يكون نفس الحساب الأصلي")
        return True
