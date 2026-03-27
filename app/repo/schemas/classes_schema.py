from .base_schema import BaseDataClass
from dataclasses import dataclass

@dataclass
class ClassesSchema(BaseDataClass):
    name: str
    way: str
    teacher: str
    note: str
    price: float
    seance: int
    exchange: str
    teacher_part: float
    
@dataclass
class EnrollmentSchema(BaseDataClass):
    student_id: int
    class_name: str