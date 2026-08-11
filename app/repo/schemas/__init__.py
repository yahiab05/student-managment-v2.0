from typing import Type

from .classes_schema import ClassesSchema, EnrollmentSchema
from .person_schema import StudentSchema, TeacherSchema, StudentHistorySchema, TeacherHistorySchema
from .money_schema import EntrySchema, ExpensesSchema
from .others_schema import RoleSchema, SettingsSchema, UserSchema


class SchemaFactory:
    """Single entry point for all schema dataclasses.

    Static use (preferred — full autocomplete on schema name and fields):
        instance = SchemaFactory.CLASSES(name="Math", ...)

    Dynamic use (name only known at runtime):
        Schema = SchemaFactory.get_schema("CLASSES")
        instance = Schema(**payload)
    """

    CLASSES = ClassesSchema
    ENROLLMENT = EnrollmentSchema
    STUDENT = StudentSchema
    TEACHER = TeacherSchema
    STUDENT_HISTORY = StudentHistorySchema
    TEACHER_HISTORY = TeacherHistorySchema
    INCOME = EntrySchema
    EXPENSES = ExpensesSchema
    ROLE = RoleSchema
    SETTINGS = SettingsSchema
    USER = UserSchema

    @classmethod
    def get_schema(cls, name: str) -> Type:
        try:
            return getattr(cls, name)
        except AttributeError:
            raise ValueError(
                f"Unknown schema: '{name}'. Available schemas: {cls.available()}"
            )

    @classmethod
    def create(cls, name: str, **kwargs):
        return cls.get_schema(name)(**kwargs)

    @classmethod
    def available(cls) -> list[str]:
        return [k for k, v in vars(cls).items() if isinstance(v, type)]