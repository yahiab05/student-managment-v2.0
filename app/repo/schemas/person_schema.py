from abc import ABC, abstractmethod
from dataclasses import dataclass
from .base_schema import BaseDataClass
from datetime import datetime

@dataclass(kw_only=True)
class PersonSchema(ABC, BaseDataClass):
    name: str
    birthday: datetime
    date_inscrit: datetime
    # optional
    note: str = ""
    
    def validate(self):
        if not super().validate():
            return False
        if self.name is None or not str(self.name).strip():
            raise ValueError("الاسم مطلوب")
        if self.birthday is None:
            raise ValueError("تاريخ الميلاد مطلوب")
        if self.date_inscrit is None:
            raise ValueError("تاريخ التسجيل مطلوب")
        return True
    
@dataclass
class StudentSchema(PersonSchema):
    num_inscrit: int = None
    gender: str
    parent: str
    cin: int
    activity: str
    num_tel: str
    excused: str
    
    def validate(self):
        if not super().validate():
            return False
        if self.num_inscrit is None:
            raise ValueError("رقم الطالب مطلوب")
        if self.gender is None or  self.gender == "":
            raise ValueError("الجنس مطلوب")
        if self.parent is None or self.parent == "":
            raise ValueError("اسم الولي مطلوب")
        if self.cin is None:
            raise ValueError("رقم الهوية مطلوب")
        if self.activity is None or self.activity == "":
            raise ValueError("النشاط مطلوب")
        if self.num_tel is None or self.num_tel == "":
            raise ValueError("رقم الهاتف مطلوب")
        return True
    
@dataclass
class TeacherSchema(PersonSchema):
    phone: str
    payed: str
    
    def validate(self):
        if not super().validate():
            return False
        if self.phone is None or self.phone == "":
            raise ValueError("رقم الهاتف مطلوب")
        if self.payed is None or self.payed == "":
            raise ValueError("الدفع مطلوب")
        return True
    
@dataclass
class HistorySchema(ABC, BaseDataClass):
    date_inscrit: datetime
    
    def validate(self):
        if not super().validate():
            return False
        if self.date_inscrit is None:
            raise ValueError("تاريخ التسجيل مطلوب")
        return True
    
@dataclass
class StudentHistorySchema(HistorySchema):
    num_inscrit: int
    
    def validate(self):
        if not super().validate():
            return False
        if self.num_inscrit is None:
            raise ValueError("رقم الطالب مطلوب")
        return True
    
@dataclass
class TeacherHistorySchema(HistorySchema):
    teacher_id: int
    
    def validate(self):
        if not super().validate():
            return False
        if self.teacher_id is None:
            raise ValueError("رقم المعلم مطلوب")
        return True