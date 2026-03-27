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
    
@dataclass
class StudentSchema(PersonSchema):
    num_inscrit: int
    gender: str
    parent: str
    cin: int
    activity: str
    num_tel: str
    excused: str
    
@dataclass
class TeacherSchema(PersonSchema):
    phone: str
    payed: str
    
    
@dataclass
class HistorySchema(ABC, BaseDataClass):
    date_inscrit: datetime
    
@dataclass
class StudentHistorySchema(HistorySchema):
    num_inscrit: int
    
@dataclass
class TeacherHistorySchema(HistorySchema):
    teacher_id: int
    payed: str