from dataclasses import asdict, dataclass
from abc import ABC, abstractmethod
from PyQt6.QtCore import QDate

@dataclass(kw_only=True)
class BaseDataClass(ABC):
    user: str
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def qtdate_to_pydate(cls, qtdate:QDate):
        return qtdate.toPyDate()
    
    @abstractmethod
    def validate(self):
        if self.user is None or self.user == "":
            raise ValueError("اسم المستخدم مطلوب")
        return True
    
    