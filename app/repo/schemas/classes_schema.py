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
    
    def validate(self):
        if not super().validate():
            return False
        if self.name is None or self.name == "":
            raise ValueError("اسم الصف مطلوب")
        if self.way is None or self.way == "":
            raise ValueError("نوع التدريس مطلوب")
        if self.teacher is None or self.teacher == "":
            raise ValueError("اسم المعلم مطلوب")
        if self.price is None or self.price == 0:
            raise ValueError("سعر الصف مطلوب")
        if self.seance is None or self.seance == 0:
            raise ValueError("عدد الحصص مطلوب")
        if self.exchange is None or self.exchange == "":
            raise ValueError("المقابل مطلوب")
        if self.teacher_part is None:
            raise ValueError("حصة المعلم مطلوبة")
        return True
    
@dataclass
class EnrollmentSchema(BaseDataClass):
    student_id: int
    class_name: str