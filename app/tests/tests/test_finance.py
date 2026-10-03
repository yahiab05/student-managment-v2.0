from unittest.mock import DEFAULT, MagicMock, patch

import pytest

from app.controllers.finance import BalanceLogic, EnteryLogic, OutMoneyLogic, TransferLogic
from app.utils import Account, ReportType, WorkingMode


def fake_load_gui(path, filename, target):
    widget_names = {
        "entery.ui": (
            "delete_btn", "update_btn", "add_btn", "tbl", "printing_btn",
            "export_btn", "bill_code", "name_search", "price_search",
            "operatore", "to", "du", "code", "type_search", "way_search",
            "total", "reset_btn", "search_btn", "select_info",
        ),
        "out.ui": (
            "delete_btn", "update_btn", "add_btn", "tbl", "printing_btn",
            "export_btn", "name_search", "price_search", "operatore", "to",
            "du", "way_search", "code", "type_search", "total", "reset_btn",
            "search_btn", "select_info",
        ),
        "solde.ui": (
            "tbl", "solde", "total_in", "total_out", "printing_btn",
            "export_btn", "price_input", "operatore", "du", "to", "way",
            "reset_btn", "search_btn",
        ),
        "transfer.ui": (
            "table", "printing_btn", "export_btn", "operatore", "to", "du",
            "reset_btn", "search_btn", "date", "price", "note",
            "to_bank_btn", "to_caisse_btn", "total_bank", "total_caisse",
        ),
    }
    for name in widget_names[filename]:
        setattr(target, name, MagicMock())
    
@pytest.fixture
def finance_dependencies():
    patches = [
        patch.multiple(
            "app.controllers.finance.income",
            load_gui=DEFAULT, get_model=DEFAULT, get_combo_manager=DEFAULT,
            create_table_model=DEFAULT, create_popup_factory=DEFAULT,
            SchemaFactory=DEFAULT, get_username=DEFAULT, error=DEFAULT,
        ),
        patch.multiple(
            "app.controllers.finance.expenses",
            load_gui=DEFAULT, get_model=DEFAULT, get_combo_manager=DEFAULT,
            create_table_model=DEFAULT, create_popup_factory=DEFAULT,
            SchemaFactory=DEFAULT, get_username=DEFAULT, error=DEFAULT,
        ),
        patch.multiple(
            "app.controllers.finance.balance",
            load_gui=DEFAULT, get_model=DEFAULT, get_combo_manager=DEFAULT,
            create_table_model=DEFAULT,
        ),
        patch.multiple(
            "app.controllers.finance.transfer",
            load_gui=DEFAULT, get_model=DEFAULT, get_combo_manager=DEFAULT,
            create_table_model=DEFAULT, SchemaFactory=DEFAULT,
            get_username=DEFAULT, error=DEFAULT,
        ),
    ]
    mocks = [item.start() for item in patches]
    mocks[0]["load_gui"].side_effect = fake_load_gui
    mocks[1]["load_gui"].side_effect = fake_load_gui
    mocks[2]["load_gui"].side_effect = fake_load_gui
    mocks[3]["load_gui"].side_effect = fake_load_gui
    try:
        model = MagicMock()
        model.get_by_filter.return_value = []
        model.get_total.return_value = 100
        model.get_balance.return_value = []
        model.get_filter.return_value = {}
        model.get_filters.return_value = ({}, {})
        model.calculate_balance.return_value = 50
        model.get_current_data.return_value = []
        model.exists.return_value = False
        model.db = model
        table_model = MagicMock()
        table_model.ID_COLUMN = 0

        for module_mocks in mocks:
            module_mocks["get_model"].side_effect = lambda _name: model
            module_mocks["get_combo_manager"].return_value = MagicMock()
            module_mocks["create_table_model"].return_value = table_model
            if "get_username" in module_mocks:
                module_mocks["get_username"].return_value = "test_user"
                entity = MagicMock()
                entity.validate.return_value = True
                module_mocks["SchemaFactory"].INCOME.return_value = entity
                module_mocks["SchemaFactory"].EXPENSES.return_value = entity
                module_mocks["SchemaFactory"].TRANSFER.return_value = entity

        yield {
            "income": mocks[0], "expenses": mocks[1], "balance": mocks[2],
            "transfer": mocks[3], "model": model, "table": table_model,
        }
    finally:
        for item in reversed(patches):
            item.stop()


def income_data():
    return {
        "name": "Salary", "date": "2026-01-01", "type": "Monthly",
        "way": "Cash", "price": 100, "note": "", "bill_number": "IN-1",
        "cheq_num": "", "code_input": 10, "in_bank": "البنك",
    }


def expense_data():
    return {
        "name": "Supplies", "bill_num": "OUT-1", "date": "2026-01-01",
        "type": "Office", "way": "Cash", "cheq_num": "", "price": 25,
        "note": "", "code": 20, "in_bank": "البنك",
    }


class TestIncomeFinanceCRUD:
    def test_create_income(self, finance_dependencies):
        logic = EnteryLogic()
        logic.manager = finance_dependencies["model"]
        logic.control(WorkingMode.ADD, income_data())
        finance_dependencies["model"].create.assert_called_once()

    def test_update_income(self, finance_dependencies):
        logic = EnteryLogic()
        logic.identifier = 7
        logic.manager = finance_dependencies["model"]
        logic.control(WorkingMode.UPDATE, income_data())
        finance_dependencies["model"].update.assert_called_once_with(
            7, finance_dependencies["income"]["SchemaFactory"].INCOME.return_value
        )

    def test_delete_income(self, finance_dependencies):
        logic = EnteryLogic()
        logic.identifier = 7
        logic.manager = finance_dependencies["model"]
        logic.delete_income()
        finance_dependencies["model"].sup_security.assert_called_once_with(
            widget=logic, id=7, text="متأكد من حذف هذا الدخل ؟"
        )

    def test_read_income(self, finance_dependencies):
        logic = EnteryLogic()
        logic.manager = finance_dependencies["model"]
        logic.show_entery()
        finance_dependencies["model"].get_by_filter.assert_called_once_with({})
        finance_dependencies["table"].refresh.assert_called_once()
        finance_dependencies["model"].get_total.assert_called_once_with({})


class TestExpenseFinanceCRUD:
    def test_create_expense(self, finance_dependencies):
        logic = OutMoneyLogic()
        logic.manager = finance_dependencies["model"]
        logic.unique = MagicMock(return_value=False)
        logic.control(WorkingMode.ADD, expense_data())
        finance_dependencies["model"].create.assert_called_once()

    def test_update_expense(self, finance_dependencies):
        logic = OutMoneyLogic()
        logic.identifier = 8
        logic.manager = finance_dependencies["model"]
        logic.control(WorkingMode.UPDATE, expense_data())
        finance_dependencies["model"].update.assert_called_once_with(
            8, finance_dependencies["expenses"]["SchemaFactory"].EXPENSES.return_value
        )

    def test_delete_expense(self, finance_dependencies):
        logic = OutMoneyLogic()
        logic.identifier = 8
        logic.manager = finance_dependencies["model"]
        logic.delete()
        finance_dependencies["model"].sup_security.assert_called_once_with(
            widget=logic, id=8, text="متأكد من حذف هذا المصروف ؟"
        )

    def test_read_expense(self, finance_dependencies):
        logic = OutMoneyLogic()
        logic.manager = finance_dependencies["model"]
        logic.show_out()
        finance_dependencies["model"].get_by_filter.assert_called_once_with({})
        finance_dependencies["table"].refresh.assert_called_once()
        finance_dependencies["model"].get_total.assert_called_once_with({})


class TestBalanceFinance:
    def test_read_balance(self, finance_dependencies):
        logic = BalanceLogic()
        logic.manager = finance_dependencies["model"]
        logic.show_table()
        finance_dependencies["model"].get_balance.assert_called_once()
        finance_dependencies["table"].refresh.assert_called_once_with([])

    def test_export_balance(self, finance_dependencies):
        logic = BalanceLogic()
        logic.model = finance_dependencies["table"]
        logic.manager = logic.income_manager = logic.expenses_manager = finance_dependencies["model"]
        logic.export(ReportType.PRINT)
        finance_dependencies["model"].set_dynamic_metadata.assert_called_once()
        finance_dependencies["model"].export_data.assert_called_once_with(
            report_type=ReportType.PRINT, parent=logic
        )


class TestTransferFinance:
    def test_create_transfer_to_bank(self, finance_dependencies):
        logic = TransferLogic()
        logic.manager = finance_dependencies["model"]
        logic.date.date.return_value.toPyDate.return_value = "2026-01-01"
        logic.price.value.return_value = 50
        logic.note.text.return_value = "Deposit"
        logic.transfer_order(Account.BANK)
        finance_dependencies["model"].create.assert_called_once()

    def test_read_transfers(self, finance_dependencies):
        logic = TransferLogic()
        logic.manager = finance_dependencies["model"]
        logic.show_table()
        finance_dependencies["model"].get_by_filter.assert_called_once_with({})
        finance_dependencies["table"].refresh.assert_called_once_with([])

    def test_export_transfers(self, finance_dependencies):
        logic = TransferLogic()
        logic.model = finance_dependencies["table"]
        logic.manager = finance_dependencies["model"]
        logic.export(ReportType.EXCEL)
        finance_dependencies["model"].set_dynamic_metadata.assert_called_once()
        finance_dependencies["model"].export_data.assert_called_once_with(
            report_type=ReportType.EXCEL, parent=logic
        )