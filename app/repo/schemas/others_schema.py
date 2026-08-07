from dataclasses import dataclass
from abc import ABC, abstractmethod
from .base_schema import BaseDataClass

@dataclass
class CommonSchema(BaseDataClass, ABC):
    @abstractmethod
    def validate(self):
        pass

@dataclass
class RoleSchema(CommonSchema):
    name:str
    classes:bool
    students:bool
    teachers:bool
    payment:bool
    money:bool
    settings:bool
    user:bool
    payment_editting:bool
    
    def validate(self):
        if self.name is None or (isinstance(self.name, str) and self.name.strip() == ""):
            raise ValueError("اسم الصلاحية مطلوب")
        if self.classes is None:
            raise ValueError("صلاحية الصف مطلوب")
        if self.students is None:
            raise ValueError("صلاحية الطلاب مطلوب")
        if self.teachers is None:
            raise ValueError("صلاحية المعلمين مطلوب")
        if self.payment is None:
            raise ValueError("صلاحية الدفع مطلوب")
        if self.money is None:
            raise ValueError("صلاحية المال مطلوب")
        if self.settings is None:
            raise ValueError("صلاحية الاعدادات مطلوب")
        if self.user is None:
            raise ValueError("صلاحية المستخدمين مطلوب") 
        if self.payment_editting is None:
            raise ValueError("صلاحية تعديل الدفع مطلوب")
        return True
    
@dataclass
class SettingsSchema(CommonSchema):
    way_teaching:str=None
    entery:str=None
    entery_code:int=None
    out_money:str=None
    out_code:int=None
    way_payment:str = None
    fr:str = None
    
    def validate(self):
        if self.entery is not None and self.entery != "":
            if self.entery_code is None:
                raise ValueError("رقم الدخول مطلوب")
        if self.out_money is not None and self.out_money != "":
            if self.out_code is None:
                raise ValueError("رقم الخروج مطلوب")
        return True
    
@dataclass
class UserSchema(CommonSchema):
    username:str
    password:str
    role_name:str
    
    def validate(self):
        if self.username is None or self.username == "":
            raise ValueError("اسم المستخدم مطلوب")
        if self.password is None or self.password == "":
            raise ValueError("كلمة المرور مطلوب")
        if self.role_name is None or self.role_name == "":
            raise ValueError("اسم الصلاحية مطلوب")
        return True