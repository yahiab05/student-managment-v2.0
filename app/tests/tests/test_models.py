from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from app.models import get_model
from app.models.admin import Login, Roles, Users
from app.models.classes import Classes, Enrollment
from app.models.finance import Balance, Expense, Income, Payment, Transfer
from app.models.names import ModelName
from app.models.person import Student, StudentHistory, Teacher, TeacherHistory
from app.models.settings import Settings
from app.repo.schemas import SchemaFactory
from app.repo.schemas.classes_schema import ClassesSchema, EnrollmentSchema
from app.repo.schemas.money_schema import ExpensesSchema, TransferSchema
from app.repo.schemas.others_schema import RoleSchema, UserSchema
from app.repo.schemas.person_schema import (
    StudentHistorySchema, StudentSchema, TeacherHistorySchema, TeacherSchema,
)


@pytest.fixture
def repository():
    repo = MagicMock()
    repo.get_repo.return_value = MagicMock()
    repo.get_balance_repo.return_value = MagicMock()
    return repo


def income_schema():
    return SchemaFactory.INCOME(
        user="tester", name="Salary", price=100, code=10, way="Cash",
        type="Monthly", in_bank=True, bill_number="IN-1",
        addition_date=date(2026, 1, 1),
    )


def expense_schema():
    return ExpensesSchema(
        user="tester", name="Supplies", price=25, code=20, way="Cash",
        type="Office", in_bank=True, bill_number="OUT-1",
        date=date(2026, 1, 1),
    )


def transfer_schema():
    return TransferSchema(
        user="tester", price=50, origin="الصندوق", destination="البنك",
        date=date(2026, 1, 1),
    )


def model_schema(model_class):
    if model_class is Classes:
        return ClassesSchema(
            user="tester", name="Class A", way="Group", teacher="Teacher",
            note="", price=100,
        )
    if model_class is Enrollment:
        return EnrollmentSchema(user="tester", student_id=1, class_name="Class A")
    if model_class in (Roles,):
        return RoleSchema(
            name="Admin", classes=True, students=True,
            teachers=True, payment=True, money=True, settings=True, user=True,
            payment_editting=True,
        )
    if model_class in (Users, Login):
        return UserSchema(
            username="admin", password="secret", role_name="Admin"
        )
    if model_class is Student:
        return StudentSchema(
            user="tester", name="Ali", birthday=date(2000, 1, 1),
            date_inscrit=date(2026, 1, 1), gender="M", parent="Parent", cin=1,
            activity="Active", num_tel="1", excused="No",
        )
    if model_class is Teacher:
        return TeacherSchema(
            user="tester", name="Teacher", birthday=date(1980, 1, 1),
            date_inscrit=date(2026, 1, 1), phone="1",
        )
    if model_class is StudentHistory:
        return StudentHistorySchema(
            user="tester", date_inscrit=date(2026, 1, 1), num_inscrit=1
        )
    if model_class is TeacherHistory:
        return TeacherHistorySchema(
            user="tester", date_inscrit=date(2026, 1, 1), teacher_id=1
        )
    return income_schema()


@pytest.mark.parametrize(
    "model_class,table",
    [(Income, ModelName.INCOME), (Expense, ModelName.EXPENSES),
    (Transfer, ModelName.TRANSFER), (Settings, "settings")],
)
def test_models_delegate_full_crud(model_class, table, repository):
    db = repository.get_repo.return_value
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        model = model_class()
        schema = (
            income_schema() if model_class is Income
            else expense_schema() if model_class is Expense
            else transfer_schema()
            if model_class is Transfer else SchemaFactory.SETTINGS(
                user="tester", way_payment="Cash"
            )
        )

        model.create(schema)
        model.get_all()
        model.get_by_id(1)
        model.get_by_filter([])
        model.exists([])
        model.update(1, schema)
        model.update_by_filter([], schema)
        model.delete(1)
        model.delete_by_filter([])
        model.get_total([])
        model.update_price(1, 75)

        db.add.assert_called_once_with(schema.to_dict(), _session=None)
        db.get_all.assert_called_once()
        db.get_by_id.assert_called_once_with(1, _session=None)
        db.get_by_filter.assert_called_once_with([])
        db.exists.assert_called_once_with([])
        db.update.assert_called_once_with(1, schema.to_dict())
        db.update_by_filter.assert_called_once_with([], schema.to_dict())
        db.delete.assert_called_once_with(1)
        db.delete_by_filter.assert_called_once_with([])
        db.get_total.assert_called_once_with([])
        db.update_price.assert_called_once_with(1, 75)


def test_crud_bulk_create_and_transaction(repository):
    db = repository.get_repo.return_value
    session = MagicMock()
    db.transaction.return_value.__enter__.return_value = session
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        model = Income()
        model.bulk_create([income_schema(), income_schema()])
        with model.transaction() as yielded:
            assert yielded is session

    db.bulk_add.assert_called_once()
    db.transaction.assert_called_once()


def test_finance_filters_and_metadata(repository):
    db = repository.get_repo.return_value
    row = MagicMock(
        price=100, way="Cash", name="Salary", type="Monthly", code=10,
        addition_date=date(2026, 1, 1), date=date(2026, 1, 1),
        bill_number="IN-1",
    )
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        income = Income()
        expense = Expense()
        payment = Payment()
        transfer = Transfer()

        assert income.get_filter(code=10, name="Salary", way="Cash", type="Monthly",
                                addition_from_date=date(2026, 1, 1),
                                addition_to_date=date(2026, 1, 2), price=10,
                                operator="=", in_bank=True)
        assert expense.get_filters(code=20, way_payment="Cash", name="Supplies",
                                    bill_number="OUT-1", type="Office",
                                    from_date=date(2026, 1, 1),
                                    to_date=date(2026, 1, 2), price=10,
                                    operator="=", in_bank=True)
        assert payment.get_filter(name="Student", way="Cash", num_inscrit=1,
                                    classroom="A", exact_date=date(2026, 1, 1),
                                    year=2026, month=1)
        assert transfer.get_filter(from_date=date(2026, 1, 1),
                                    to_date=date(2026, 1, 2), price=10,
                                    operator="=", destination="bank")
        assert transfer.get_filter(from_date=date(2026, 1, 1),
                                    to_date=date(2026, 1, 2), price=10,
                                    operator="=", origin="bank")

        income.set_dynamic_metadata(100, [row])
        expense.set_dynamic_metadata(25, [row])
        payment.set_dynamic_metadata(25, [row])
        transfer.set_dynamic_metadata(50, [row])

    assert income.data_to_export and expense.data_to_export
    assert payment.data_to_export and transfer.data_to_export


def test_settings_code_and_type_lookup(repository):
    db = repository.get_repo.return_value
    setting = MagicMock(entery_code=10, out_code=20, entery="Salary", out_money="Supplies")
    db.get_by_filter.return_value = [setting]
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        model = Settings()
        assert model.get_code("Salary", None) == 10
        assert model.get_code(None, "Supplies") == 20
        assert model.get_type(10, None) == "Salary"
        assert model.get_type(None, 20) == "Supplies"


def test_balance_model_operations(repository):
    balance_repo = repository.get_balance_repo.return_value
    balance_repo.get_filters.return_value = (["income"], ["expense"])
    balance_repo.get_balance.return_value = ["row"]
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        model = Balance()
        assert model.calculate_balance(100, 25) == 75
        assert model.get_balance("Cash") == ["row"]
    balance_repo.get_balance.assert_called_once()


@pytest.mark.parametrize(
    "model_class",
    [Classes, Enrollment, Roles, Users, Login, Student, Teacher,
    TeacherHistory, StudentHistory, Payment],
)
def test_remaining_models_expose_crud(model_class, repository):
    db = repository.get_repo.return_value
    payload = model_schema(model_class)
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        model = model_class()
        model.create(payload)
        model.bulk_create([payload])
        model.get_all()
        model.get_by_id(1)
        model.get_by_filter([])
        if isinstance(model, Student):
            model.exists(name=payload.name, parent=payload.parent)
        else:
            model.exists([])
        model.update(1, payload)
        model.update_by_filter([], payload)
        if isinstance(model, Student):
            with patch.object(model, "permenant", return_value=False):
                model.delete(1)
                assert not db.delete.called
            
            with patch.object(model, "permenant", return_value=True):
                model.delete(1)
                assert db.delete.called
        else:
            model.delete(1)
        model.delete_by_filter([])
        model.get_total([])
        model.update_price(1, 5)

    assert db.add.called
    assert db.bulk_add.called
    assert db.update.called
    assert db.delete.called


def test_access_manager_loads_and_caches_permissions(repository):
    user = MagicMock(role_name="admin")
    role = MagicMock(
        students=True, classes=True, teachers=False, payment=True,
        money=False, settings=True, user=False, payment_editting=True,
    )
    db = repository.get_repo.return_value
    db.get_by_filter.side_effect = [[user], [role]]
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        from app.models.access_manager import AccessManager

        manager = AccessManager()
        manager.set_user("tester")
        assert manager.get_access("students") is True
        assert manager.get_access("teachers") is False
        assert manager.get_access("unknown") is False
        assert manager.get_access("students") is True


def test_login_model_checks_credentials(repository):
    db = repository.get_repo.return_value
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        model = Login()
        db.exists.side_effect = [True, True]
        assert model.check_login("admin", "secret") == (True, 0)
        db.exists.side_effect = [False]
        assert model.check_login("missing", "secret") == (False, 1)
        db.exists.side_effect = [True, False]
        assert model.check_login("admin", "wrong") == (False, 2)


def test_model_factory_resolves_aliases_and_rejects_unknown(repository):
    with patch("app.models.basic_operations.Repositories", return_value=repository):
        assert type(get_model(ModelName.INCOME)) is Income
        assert type(get_model("expenses")) is Expense
        with pytest.raises(ValueError):
            get_model("not-a-model")
