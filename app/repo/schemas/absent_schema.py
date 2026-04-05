from abc import ABC, abstractmethod
from dataclasses import dataclass
from .base_schema import BaseDataClass
from datetime import datetime

@dataclass
class AbsentSchema(ABC, BaseDataClass):
    num_inscrit: int
    class_ab: str
    date_ab: datetime
    du: datetime
    time_last: datetime
    
    @abstractmethod
    def validate(self):
        if not super().validate():
            return False
        if self.num_inscrit is None:
            raise ValueError("رقم الطالب مطلوب")
        if self.class_ab is None or self.class_ab == "":
            raise ValueError("اسم الصف مطلوب")
        if self.date_ab is None:
            raise ValueError("تاريخ الغياب مطلوب")
        if self.du is None:
            raise ValueError("بداية الحصة مطلوب")
        if self.time_last is None:
            raise ValueError("نهاية الحصة مطلوب")
        
        return True
    
@dataclass
class AbsentTSchema(AbsentSchema):
    rep: str = ""
    date_rep: datetime | None
    
    def validate(self):
        if not super().validate():
            return False
        if self.rep is None:
            raise ValueError("اسم المعوض مطلوب")
        if self.date_rep is None and self.rep != "":
            raise ValueError("تاريخ التعويض مطلوب")
        if self.rep == "":
            self.date_rep = None
        return True
    
@dataclass
class AbsentSSchema(AbsentSchema):
    def validate(self):
        return super().validate()