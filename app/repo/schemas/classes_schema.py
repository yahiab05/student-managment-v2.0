from .base_schema import BaseDataClass

class ClassesSchema(BaseDataClass):
    name: str
    way: str
    teacher: str
    note: str
    price: float
    seance: int
    exchange: str
    teacher_part: float
    
class EnrollmentSchema(BaseDataClass):
    student_id: int
    class_name: str