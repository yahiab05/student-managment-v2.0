from .absent_schema import AbsentSSchema, AbsentTSchema
from .classes_schema import ClassesSchema, EnrollmentSchema
from .person_schema import StudentSchema, TeacherSchema, StudentHistorySchema, TeacherHistorySchema
from .money_schema import EntrySchema, ExpensesSchema, StorageSchema
from .others_schema import RoleSchema, SettingsSchema, UserSchema
from enum import Enum
from typing import Type


class SchemaFactory(Enum):
    ABSENT_S = AbsentSSchema
    ABSENT_T = AbsentTSchema
    CLASSES = ClassesSchema
    ENROLLMENT = EnrollmentSchema
    STUDENT = StudentSchema
    TEACHER = TeacherSchema
    STUDENT_HISTORY = StudentHistorySchema
    TEACHER_HISTORY = TeacherHistorySchema
    INCOME = EntrySchema
    EXPENSES = ExpensesSchema
    STORAGE = StorageSchema
    ROLE = RoleSchema
    SETTINGS = SettingsSchema
    USER = UserSchema
    
    def __init__(self, schema_class):
        self._schema_class = schema_class
        self._instance = None
        
    @property
    def instance(self):
        return self._instance
    
    @property
    def schema_class(self) -> Type:
        return self._schema_class
    
    def create(self, **kwargs):
        self._instance = self.schema_class(**kwargs)
    
