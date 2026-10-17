from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest

from app.repo.facade import BalanceFacade, DBFacade
from app.repo import Repositories
from app.repo.schemas import SchemaFactory
from app.repo.schemas.classes_schema import ClassesSchema, EnrollmentSchema
from app.repo.schemas.others_schema import RoleSchema, SettingsSchema, UserSchema
from app.repo.schemas.person_schema import (
    StudentHistorySchema, StudentSchema, TeacherHistorySchema, TeacherSchema,
)


class FakeQuery:
    def __init__(self, result=None):
        self.result = result or []

    def filter(self, *filters):
        return self

    def all(self):
        return self.result or []

    def first(self):
        return self.result[0] if self.result else None

    def scalar(self):
        return self.result[0] if self.result else None

    def with_entities(self, *_entities):
        return self

    def options(self, *_options):
        return self

    def order_by(self, *_columns):
        return self


class FakeSession:
    def __init__(self, result=None, fail=False):
        self.result = result
        self.fail = fail
        self.committed = False
        self.rolled_back = False
        self.deleted = None

    def __enter__(self):
        
        return self

    def __exit__(self, *_args):
        return False

    def query(self, *_entities):
        return FakeQuery(self.result)

    def add(self, obj):
        if self.fail:
            raise RuntimeError("add failed")
        self.added = obj

    def bulk_save_objects(self, objects):
        self.added = objects

    def delete(self, obj):
        self.deleted = obj

    def commit(self):
        self.committed = True
        if self.fail:
            raise RuntimeError("commit failed")

    def rollback(self):
        self.rolled_back = True


@pytest.fixture
def facade():
    table = MagicMock()
    
    def create_model(**kwargs):
        obj = MagicMock()

        for key, value in kwargs.items():
            setattr(obj, key, value)

        return obj
    
    table.side_effect = create_model
    
    return DBFacade(table), table


def test_db_facade_crud_and_queries(facade):
    repo, table = facade
    obj = MagicMock(id=1, price=10)
    session = FakeSession(result=[obj])
    with patch("app.repo.facade.SessionLocal", return_value=session):
        data = {"name": "Salary", "price": 10}
        assert repo.add(data).name == "Salary"
        multiple_data = [{"name": "Salary", "price": 10}, {"name": "Bonus", "price": 20}]
        repo.bulk_add(multiple_data)
        assert repo.get_all() == [obj]
        assert repo.get_by_id(1) == obj
        assert repo.get_by_id(1, multiple=True) == [obj]
        assert repo.get_biggest_id() == obj
        assert repo.get_by_filter([]) == [obj]
        assert repo.exists([])
        assert repo.get_total([]) == obj
        assert repo.update(1, data) == obj
        assert repo.update_by_filter([], data) == obj
        repo.delete(1)
        repo.delete_by_filter([])
        assert repo.update_price(1, 75) == obj


def test_db_facade_error_paths_and_transaction(facade):
    repo, _ = facade
    session = FakeSession(result=None)
    with patch("app.repo.facade.SessionLocal", return_value=session):
        with pytest.raises(ModuleNotFoundError):
            repo.update(1, {})
        with pytest.raises(ModuleNotFoundError):
            repo.delete(1)
        with pytest.raises(ModuleNotFoundError):
            repo.update_by_filter([], {})
        with pytest.raises(ModuleNotFoundError):
            repo.delete_by_filter([])

    failing = FakeSession(fail=True)
    with patch("app.repo.facade.SessionLocal", return_value=failing):
        with pytest.raises(RuntimeError):
            repo.add({})
        with pytest.raises(RuntimeError):
            with repo.transaction():
                raise RuntimeError("transaction failed")
    assert failing.rolled_back


def test_repositories_mapping_and_balance_filters():
    with patch("app.repo.Repositories.__init__", return_value=None):
        repos = Repositories.__new__(Repositories)
        repos._map = {"income": "income_repo", "balance": "balance_repo"}
        repos.balance = "balance_repo"
        assert repos.get_repo("income") == "income_repo"
        assert repos.get_repo("balance") is None
        assert repos.get_balance_repo() == "balance_repo"


def test_balance_facade_builds_income_and_expense_filters():
    facade = BalanceFacade()
    income, expense = facade.get_filters(
        way_payment="Cash", from_date="2026-01-01", to_date="2026-01-02",
        price=10, operator="="
    )
    assert len(income) == 3
    assert len(expense) == 3


def test_schema_factory_and_crud_payloads():
    schema = SchemaFactory.create(
        "SETTINGS", user="tester", way_payment="Cash"
    )
    assert schema.to_dict()["way_payment"] == "Cash"
    assert "SETTINGS" in SchemaFactory.available()
    with pytest.raises(ValueError):
        SchemaFactory.get_schema("UNKNOWN")


@pytest.mark.parametrize(
    "schema",
    [
        ClassesSchema(
            user="tester", name="A", way="Group", teacher="T", note="", price=10
        ),
        EnrollmentSchema(user="tester", student_id=1, class_name="A"),
        StudentSchema(
            user="tester", name="Ali", birthday="2000-01-01",
            date_inscrit="2026-01-01", gender="M", parent="Parent", cin=1,
            activity="Active", num_tel="1", excused="No",
        ),
        TeacherSchema(
            user="tester", name="Teacher", birthday="1980-01-01",
            date_inscrit="2026-01-01", phone="1",
        ),
        StudentHistorySchema(user="tester", date_inscrit="2026-01-01", num_inscrit=1),
        TeacherHistorySchema(user="tester", date_inscrit="2026-01-01", teacher_id=1),
        RoleSchema(
            name="Admin", classes=True, students=True, teachers=True,
            payment=True, money=True, settings=True, user=True,
            payment_editting=True,
        ),
        SettingsSchema(user="tester", way_payment="Cash"),
        UserSchema(username="admin", password="secret", role_name="Admin"),
    ],
)
def test_schema_dummy_data_validates_and_serializes(schema):
    assert schema.validate() is True
    if not isinstance(schema, (RoleSchema, UserSchema)):
        assert schema.to_dict()["user"] == "tester"
