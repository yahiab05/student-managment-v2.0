from .absent_schema import AbsentSSchema, AbsentTSchema
from .classes_schema import ClassesSchema, EnrollmentSchema
from .person_schema import StudentSchema, TeacherSchema, StudentHistorySchema, TeacherHistorySchema
from .money_schema import EntrySchema, ExpensesSchema, StorageSchema
from .others_schema import RoleSchema, SettingsSchema, UserSchema
from enum import Enum
from typing import Type


class SchemaFactory:
    pass
    