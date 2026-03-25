from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class CommonSchema:
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
    absent:bool
    settings:bool
    user:bool
    payment_editting:bool
    
@dataclass
class SettingsSchema(CommonSchema):
    way_teaching:str=None
    entery:str=None
    entery_code:int=None
    out_money:str=None
    out_code:int=None
    way_payment:str = None
    fr:str = None
    
@dataclass
class UserSchema(CommonSchema):
    username:str
    password:str
    role_name:str