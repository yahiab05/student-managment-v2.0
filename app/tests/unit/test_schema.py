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




