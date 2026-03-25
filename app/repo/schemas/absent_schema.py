from abc import ABC, abstractmethod
from dataclasses import dataclass
from .base_schema import BaseDataClass
from datetime import datetime

@dataclass
class AbsentSchema(BaseDataClass):
    num_inscrit: int
    class_ab: str
    date_ab: datetime
    du: datetime
    time_last: datetime
    
@dataclass
class AbsentTSchema(AbsentSchema):
    rep: str
    date_rep: datetime
    
@dataclass
class AbsentSSchema(AbsentSchema):
    def validate(self):
        pass