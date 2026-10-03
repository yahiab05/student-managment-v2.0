# test_settings.py

import pytest

from unittest.mock import DEFAULT, MagicMock, patch
from PyQt6.QtWidgets import QTableWidgetItem

from app.controllers.others.settings import (
    IncomeSettings,
    ExpenseSettings,
    SettingsWithoutCode,
    WaySettings,
    PaymentSettings,
    FournisseurSettings,
)
from app.utils import WorkingMode, ComboName


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_button():
    """Create a fake Qt button with the API used by setup()."""
    button = MagicMock()
    button.clicked = MagicMock()
    button.clicked.connect = MagicMock()
    return button


def make_line_edit():
    """Fake QLineEdit-like widget."""
    widget = MagicMock()
    widget.text = MagicMock(return_value="")
    widget.setText = MagicMock()
    widget.textChanged = MagicMock()
    widget.textChanged.connect = MagicMock()
    return widget


def make_spin_box():
    """Fake QSpinBox-like widget."""
    widget = MagicMock()
    widget.value = MagicMock(return_value=0)
    widget.setValue = MagicMock()
    return widget


def make_list_widget():
    """Fake QListWidget/QTableWidget-like widget."""
    widget = MagicMock()

    widget.currentRow = MagicMock(return_value=0)
    widget.currentItem = MagicMock()
    widget.item = MagicMock()
    widget.setItem = MagicMock()
    widget.addItem = MagicMock()

    widget.doubleClicked = MagicMock()
    widget.doubleClicked.connect = MagicMock()

    return widget


def fake_load_gui(_path, ui_file, target):
    """
    Fake load_gui().

    We don't load real .ui files in unit tests.
    Instead, create only the widgets required by the controller.
    """

    # Common widgets used by BaseSettings.setup()
    target.reset_btn = make_button()
    target.add_btn = make_button()
    target.update_btn = make_button()
    target.delete_btn = make_button()

    target.list = make_list_widget()
    target.entery = make_line_edit()

    # Widgets specific to SettingWithCodeFormUI
    if ui_file == "setting_with_code_form.ui":
        target.code = make_spin_box()

    # Common counter label
    target.nb = MagicMock()
    target.nb.setText = MagicMock()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_settings_deps():

    with patch.multiple(
        "app.controllers.others.settings",

        load_gui=DEFAULT,
        get_model=DEFAULT,
        get_combo_manager=DEFAULT,
        error=DEFAULT,
        SchemaFactory=DEFAULT,
        get_username=DEFAULT,

    ) as mocks:

        mock_load = mocks["load_gui"]
        mock_get_model = mocks["get_model"]
        mock_combo = mocks["get_combo_manager"]
        mock_error = mocks["error"]
        mock_schema = mocks["SchemaFactory"]

        # ---------------------------------------------------------------
        # Fake UI loader
        # ---------------------------------------------------------------

        mock_load.side_effect = fake_load_gui

        # ---------------------------------------------------------------
        # Username
        # ---------------------------------------------------------------

        mocks["get_username"].return_value = "test_user"

        # ---------------------------------------------------------------
        # Model
        # ---------------------------------------------------------------

        mock_model = MagicMock()

        mock_model.create = MagicMock()
        mock_model.update = MagicMock()
        mock_model.update_by_filter = MagicMock()

        mock_model.delete = MagicMock()
        mock_model.delete_by_filter = MagicMock()

        mock_model.get_filter = MagicMock(return_value={})
        mock_model.get_by_filter = MagicMock(return_value=[])

        mock_model.exists = MagicMock(return_value=False)
        mock_model.check_used = MagicMock(return_value=False)

        mock_model.update_cache_from_db = MagicMock()

        mock_model.get_access = MagicMock(return_value=True)

        def get_model_side_effect(name):
            if name in (
                "SETTINGS",
                "INCOME",
                "EXPENSE",
                "CLASSES",
            ):
                return mock_model

            return MagicMock()

        mock_get_model.side_effect = get_model_side_effect

        # ---------------------------------------------------------------
        # Combo manager
        # ---------------------------------------------------------------

        mock_combo_mgr = MagicMock()

        mock_combo_mgr.update_combo = MagicMock()
        mock_combo_mgr.update_cache_from_db = MagicMock()

        mock_combo.return_value = mock_combo_mgr

        # ---------------------------------------------------------------
        # Schema
        # ---------------------------------------------------------------

        mock_entity = MagicMock()
        mock_entity.validate = MagicMock(return_value=True)

        mock_schema.SETTINGS.return_value = mock_entity

        yield {
            "load": mock_load,
            "get_model": mock_get_model,
            "combo": mock_combo_mgr,
            "error": mock_error,
            "schema": mock_schema,
            "model": mock_model,
        }


# ===========================================================================
# IncomeSettings
# ===========================================================================

class TestIncomeSettings:

    def test_init(self, mock_settings_deps):

        inc = IncomeSettings()

        mock_settings_deps["load"].assert_called_once()

        assert inc.income is True
        assert inc.identifier is None

    def test_control_add(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.entery.text.return_value = "Salary"
        inc.code.value.return_value = 123

        inc.control(WorkingMode.ADD)

        mock_settings_deps["model"].create.assert_called_once()

        mock_settings_deps["combo"].update_cache_from_db.assert_called_once_with(
            ComboName.INCOME
        )

    def test_control_update(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.identifier = 1
        inc.entery.text.return_value = "Salary"
        inc.code.value.return_value = 123

        inc.control(WorkingMode.UPDATE)

        mock_settings_deps["model"].update.assert_called_once_with(
            1,
            mock_settings_deps["schema"].SETTINGS.return_value,
        )

    def test_control_validation_failure(self, mock_settings_deps):

        inc = IncomeSettings()

        mock_settings_deps["schema"].SETTINGS.return_value.validate.return_value = (
            False
        )

        inc.control(WorkingMode.ADD)

        mock_settings_deps["error"].assert_called_once_with(
            "Verifier les données"
        )

        mock_settings_deps["model"].create.assert_not_called()

    def test_delete_success(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.identifier = 1
        inc.entery.text.return_value = "Salary"

        inc.check_used = MagicMock(return_value=False)

        inc.delete()

        mock_settings_deps["model"].delete.assert_called_once_with(1)

        assert inc.identifier is None

    def test_delete_used(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.identifier = 1
        inc.entery.text.return_value = "Salary"

        inc.check_used = MagicMock(return_value=True)

        inc.delete()

        mock_settings_deps["error"].assert_called_once_with(
            "لا يمكن الحذف لأنه يتم إستعماله"
        )

        mock_settings_deps["model"].delete.assert_not_called()

    def test_check_used(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.check_used(123)

        mock_settings_deps["model"].check_used.assert_called_once_with(123)

    def test_show_data(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.show_data("Salary")

        mock_settings_deps["model"].get_filter.assert_called_once_with(
            entery="Salary"
        )

    def test_select_row(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.list.currentRow.return_value = 0

        inc.list.item.side_effect = [
            MagicMock(text=MagicMock(return_value="1")),
            MagicMock(text=MagicMock(return_value="Salary")),
            MagicMock(text=MagicMock(return_value="123")),
        ]

        inc.select_row()

        assert inc.identifier == 1
        inc.entery.setText.assert_called_once_with("Salary")
        inc.code.setValue.assert_called_once_with(123)

    def test_reset_entries(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.reset_enteries()

        inc.code.setValue.assert_called_once_with(0)
        inc.entery.setText.assert_called_once_with("")

    def test_show_table_data(self, mock_settings_deps):

        inc = IncomeSettings()

        mock_data = [
            MagicMock(
                id=1,
                out_money="Rent",
                out_code=456,
            )
        ]

        mock_settings_deps["model"].get_by_filter.return_value = mock_data

        inc.show_data({})

        assert inc.nb.setText.called

    # Keep this test only if show_data() is responsible for populating
    # the table in your actual implementation.
    def test_model_access(self, mock_settings_deps):

        inc = IncomeSettings()

        inc.show_data("Salary")

        mock_settings_deps["model"].get_filter.assert_called_once_with(
            entery="Salary"
        )


# ===========================================================================
# ExpenseSettings
# ===========================================================================

class TestExpenseSettings:

    def test_init(self, mock_settings_deps):

        exp = ExpenseSettings()

        mock_settings_deps["load"].assert_called_once()

        assert exp.income is False
        assert exp.identifier is None

    def test_check_used(self, mock_settings_deps):

        exp = ExpenseSettings()

        exp.check_used(456)

        mock_settings_deps["model"].check_used.assert_called_once_with(456)

    def test_show_data(self, mock_settings_deps):

        exp = ExpenseSettings()

        exp.show_data("Rent")

        mock_settings_deps["model"].get_filter.assert_called_once_with(
            out_money="Rent"
        )

    def test_control_add(self, mock_settings_deps):

        exp = ExpenseSettings()

        exp.entery.text.return_value = "Rent"
        exp.code.value.return_value = 456

        exp.control(WorkingMode.ADD)

        mock_settings_deps["model"].create.assert_called_once()

        mock_settings_deps["combo"].update_cache_from_db.assert_called_once_with(
            ComboName.EXPENSES
        )

    def test_control_update(self, mock_settings_deps):

        exp = ExpenseSettings()

        exp.identifier = 1
        exp.entery.text.return_value = "Rent"
        exp.code.value.return_value = 456

        exp.control(WorkingMode.UPDATE)

        mock_settings_deps["model"].update.assert_called_once()


# ===========================================================================
# WaySettings
# ===========================================================================

class TestWaySettings:

    def test_init(self, mock_settings_deps):

        way = WaySettings()

        mock_settings_deps["load"].assert_called_once()

        assert way.setting == ComboName.WAY_TEACHING

    def test_control_add(self, mock_settings_deps):

        way = WaySettings()

        way.entery.text.return_value = "Online"

        way.control(WorkingMode.ADD)

        mock_settings_deps["model"].create.assert_called_once()

        mock_settings_deps["combo"].update_cache_from_db.assert_called_once_with(
            ComboName.WAY_TEACHING
        )

    def test_control_update(self, mock_settings_deps):

        way = WaySettings()

        way.entery.text.return_value = "Online"

        way.control(WorkingMode.UPDATE)

        mock_settings_deps["model"].update_by_filter.assert_called_once()

        mock_settings_deps["combo"].update_cache_from_db.assert_called_once_with(
            ComboName.WAY_TEACHING
        )

    def test_invalid_setting(self, mock_settings_deps):

        # Bypass __init__ deliberately because we are testing the
        # validation branch inside control(), not construction.
        way = SettingsWithoutCode.__new__(SettingsWithoutCode)

        way.setting = "invalid"
        way.entery = make_line_edit()
        way.manager = mock_settings_deps["model"]

        way.control(WorkingMode.ADD)

        mock_settings_deps["error"].assert_called_once_with(
            "Invalid setting type"
        )

    def test_delete_success(self, mock_settings_deps):

        way = WaySettings()

        way.entery.text.return_value = "Online"
        way.check_used = MagicMock(return_value=False)

        way.delete()

        mock_settings_deps["model"].delete_by_filter.assert_called_once()

        mock_settings_deps["combo"].update_cache_from_db.assert_called_once_with(
            ComboName.WAY_TEACHING
        )

    def test_delete_used(self, mock_settings_deps):

        way = WaySettings()

        way.entery.text.return_value = "Online"
        way.check_used = MagicMock(return_value=True)

        way.delete()

        mock_settings_deps["error"].assert_called_once_with(
            "لا يمكن الحذف لأنه يتم إستعماله"
        )

        mock_settings_deps["model"].delete_by_filter.assert_not_called()

    def test_check_used(self, mock_settings_deps):

        way = WaySettings()

        way.check_used("Online")

        mock_settings_deps["model"].get_filters.assert_called_once_with(
            way_teaching="Online"
        )

        mock_settings_deps["model"].exists.assert_called()

    def test_show_data(self, mock_settings_deps):

        way = WaySettings()

        way.show_data("Online")

        mock_settings_deps["model"].get_filter.assert_called_once_with(
            way_teaching="Online"
        )

    def test_select_row(self, mock_settings_deps):

        way = WaySettings()

        item = MagicMock()
        item.text.return_value = "Online"

        way.list.currentItem.return_value = item

        way.way_select_row()

        way.entery.setText.assert_called_once_with("Online")


# ===========================================================================
# PaymentSettings
# ===========================================================================

class TestPaymentSettings:

    def test_check_used(self, mock_settings_deps):

        pay = PaymentSettings()

        pay.used_per_model = MagicMock(return_value=False)

        result = pay.check_used("Cash")

        assert result is False

        pay.used_per_model.assert_any_call("INCOME", "Cash")
        pay.used_per_model.assert_any_call("EXPENSE", "Cash")

    def test_used_per_model(self, mock_settings_deps):

        pay = PaymentSettings()

        pay.used_per_model("INCOME", "Cash")

        mock_settings_deps["model"].get_filter.assert_called_once_with(
            way_payment="Cash"
        )

        mock_settings_deps["model"].exists.assert_called()

    def test_show_data(self, mock_settings_deps):

        pay = PaymentSettings()

        pay.payment_show("Cash")

        mock_settings_deps["model"].get_filter.assert_called_once_with(
            way_payment="Cash"
        )


# ===========================================================================
# FournisseurSettings
# ===========================================================================

class TestFournisseurSettings:

    def test_check_used(self, mock_settings_deps):

        supplier = FournisseurSettings()

        supplier.fournisseur_check_used("Supplier")

        mock_settings_deps["model"].get_filters.assert_called_once_with(
            name="Supplier"
        )

        mock_settings_deps["model"].exists.assert_called()

    def test_show_data(self, mock_settings_deps):

        supplier = FournisseurSettings()

        supplier.fournisseur_show("Supplier")

        mock_settings_deps["model"].get_filter.assert_called_once_with(
            fr="Supplier"
        )