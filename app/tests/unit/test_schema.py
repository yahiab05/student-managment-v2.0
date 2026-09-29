<<<<<<< HEAD
from app.repo.schemas import SchemaFactory
from app.repo.schemas import (
    AbsentSSchema,
    AbsentTSchema,
    ClassesSchema,
    EnrollmentSchema,
    StudentSchema,
    TeacherSchema,
    StudentHistorySchema,
    TeacherHistorySchema,
    EntrySchema,
    ExpensesSchema,
    StorageSchema,
    RoleSchema,
    SettingsSchema,
    UserSchema,
)
import pytest

@pytest.mark.parametrize("schema_factory_member, expected_schema", [
    (SchemaFactory.ABSENT_S, AbsentSSchema),
    (SchemaFactory.ABSENT_T, AbsentTSchema),
    (SchemaFactory.CLASSES, ClassesSchema),
    (SchemaFactory.ENROLLMENT, EnrollmentSchema),
    (SchemaFactory.STUDENT, StudentSchema),
    (SchemaFactory.TEACHER, TeacherSchema),
    (SchemaFactory.STUDENT_HISTORY, StudentHistorySchema),
    (SchemaFactory.TEACHER_HISTORY, TeacherHistorySchema),
    (SchemaFactory.INCOME, EntrySchema),
    (SchemaFactory.EXPENSES, ExpensesSchema),
    (SchemaFactory.STORAGE, StorageSchema),
    (SchemaFactory.ROLE, RoleSchema),
    (SchemaFactory.SETTINGS, SettingsSchema),
    (SchemaFactory.USER, UserSchema)
    ])
def test_schema_class_function(schema_factory_member, expected_schema):
    assert schema_factory_member.value == expected_schema
    
def test_create_function_with_args():
    schema = SchemaFactory.ABSENT_S
    schema.create(
        num_inscrit=1,
        class_ab="A",
        date_ab="2022-01-01",
        du="00:00",
        time_last="00:00",
        user="user"
    )
    

    assert schema.schema_class().to_dict() == {
        "num_inscrit": 1,
        "class_ab": "A",
        "date_ab": "2022-01-01",
        "du": "00:00",
        "time_last": "00:00",
        "user": "user"
    }

@pytest.mark.parametrize("schema_factory_member, expected_schema, optional_args, default_args", [
    (SchemaFactory.ABSENT_S, {
        "num_inscrit": 1,
        "class_ab": "A",
        "date_ab": "2022-01-01",
        "du": "00:00",
        "time_last": "00:00",
        "user": "user",
    }, None, None),
    (SchemaFactory.ABSENT_T, {
        "num_inscrit": 1,
        "class_ab": "A",
        "date_ab": "2022-01-01",
        "du": "00:00",
        "time_last": "00:00",
        "user": "user",
    }, 
    {
        "rep": "test",
        "date_rep": None
    },
    {
        "rep": "",
        "date_rep": None
    }),
    (SchemaFactory.CLASSES, {
        "name": "test",
        "way": "test",
        "teacher": "test",
        "note": "test",
        "price": 1.55,
        "seance": 1,
        "exchange": "test",
        "teacher_part": 1.55,
        "user": "user"
    }, None, None),
    (SchemaFactory.ENROLLMENT, {
        "student_id": 1,
        "class_name": "test",
        "user": "user"
    }, None, None),
    (SchemaFactory.STUDENT, {
        "num_inscrit": 1,
        "name": "test",
        "birthday": "2022-01-01",
        "parent": "test",
        "num_tel": "test",
        "date_inscrit": "2022-01-01",
        "cin": 1254668,
        "activity": "test",
        "excused": "test",
        "user"  : "user",
        "gender": "male"
    }, 
    {
        "note": ""
    }, 
    {
        "note": "test"
    }),
    (SchemaFactory.TEACHER,
    {
        "name": "Ali",
        "birthday": "2022-01-01",
        "date_inscrit": "2022-01-01",
        "phone": "20020014",
        "payed": "test",
        "user": "user"
    },
    {
        "note": ""
    },
    {   
        "note": "test"
    }),
    (SchemaFactory.STUDENT_HISTORY, {
        "num_inscrit": 1,
        "date_inscrit": "2022-01-01",
        "user": "user"
    }, None, None),
    (SchemaFactory.TEACHER_HISTORY, {
        "teacher_id": 1,
        "payed": "test",
        "user": "user",
        "date_inscrit": "2022-01-01"
    }, None, None),
    (SchemaFactory.INCOME, {
        "name": "Ali",
        "price": 100.52,
        "code": 13,
        "user": "user",
        "way": "way1",
        "type": "type1",
        "bill_number": "12548dd",
=======
from datetime import date

import pytest

from app.repo.schemas import SchemaFactory
from app.repo.schemas.classes_schema import ClassesSchema
from app.repo.schemas.money_schema import TransferSchema
from app.repo.schemas.others_schema import RoleSchema, SettingsSchema
from app.repo.schemas.person_schema import StudentSchema
from app.utils import Account


def test_schema_factory_available_contains_core_schemas():
    available = SchemaFactory.available()
    assert "CLASSES" in available
    assert "ROLE" in available
    assert "INCOME" in available


def test_schema_factory_get_schema_and_create():
    schema_cls = SchemaFactory.get_schema("CLASSES")
    assert schema_cls is ClassesSchema

    obj = SchemaFactory.create(
        "CLASSES",
        name="A",
        way="offline",
        teacher="T",
        note="",
        price=120,
        user="admin",
    )
    assert isinstance(obj, ClassesSchema)
    assert obj.validate() is True


def test_schema_factory_unknown_raises():
    with pytest.raises(ValueError):
        SchemaFactory.get_schema("DOES_NOT_EXIST")


def test_role_schema_validation_required_fields():
    with pytest.raises(ValueError):
        RoleSchema(
            user="admin",
            name="",
            classes=True,
            students=True,
            teachers=True,
            payment=True,
            money=True,
            settings=True,
            user=True,
            payment_editting=True,
        ).validate()


def test_settings_schema_requires_codes_when_values_present():
    with pytest.raises(ValueError):
        SettingsSchema(user="u", entery="Income type", entery_code=None).validate()

    with pytest.raises(ValueError):
        SettingsSchema(user="u", out_money="Expense type", out_code=None).validate()


def test_student_schema_requires_id_and_core_fields():
    with pytest.raises(ValueError):
        StudentSchema(
            user="u",
            name="Student",
            birthday=date(2010, 1, 1),
            date_inscrit=date(2020, 1, 1),
            gender="M",
            parent="P",
            cin=1,
            activity="active",
            num_tel="111",
            excused="no",
            id=None,
        ).validate()


def test_transfer_schema_prevents_same_origin_and_destination():
    with pytest.raises(ValueError):
        TransferSchema(
            user="u",
            price=100,
            origin=Account.BANK,
            destination=Account.BANK,
            date=date(2025, 1, 1),
        ).validate()



>>>>>>> feature/controllers

