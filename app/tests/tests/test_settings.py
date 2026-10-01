# test_settings.py
import pytest
from unittest.mock import DEFAULT, MagicMock, patch
from PyQt6.QtWidgets import QTableWidgetItem

from app.controllers.others.settings import (
    BaseSettings, SettingsWithCode, IncomeSettings, ExpenseSettings,
    SettingsWithoutCode, WaySettings, PaymentSettings, FournisseurSettings,
    SettingsLogic
)
from app.utils import WorkingMode, ComboName


@pytest.fixture(autouse=True)
def mock_settings_deps():
    with patch.multiple(
        'app.controllers.others.settings',
        load_gui=DEFAULT,
        get_model=DEFAULT,
        get_combo_manager=DEFAULT,
        error=DEFAULT,
        SchemaFactory=DEFAULT,
        get_username=DEFAULT,
    ) as settings_mocks:
        mock_load = settings_mocks['load_gui']
        mock_get_model = settings_mocks['get_model']
        mock_combo = settings_mocks['get_combo_manager']
        mock_error = settings_mocks['error']
        mock_schema = settings_mocks['SchemaFactory']
        settings_mocks['get_username'].return_value = 'test_user'
        
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
            if name in ['SETTINGS', 'INCOME', 'EXPENSE', 'CLASSES']:
                return mock_model
            return MagicMock()
        mock_get_model.side_effect = get_model_side_effect

        mock_combo_mgr = MagicMock()
        mock_combo_mgr.update_combo = MagicMock()
        mock_combo_mgr.update_cache_from_db = MagicMock()
        mock_combo.return_value = mock_combo_mgr

        mock_entity = MagicMock()
        mock_entity.validate = MagicMock(return_value=True)
        mock_schema.SETTINGS.return_value = mock_entity

        yield {
            'load': mock_load,
            'get_model': mock_get_model,
            'combo': mock_combo_mgr,
            'error': mock_error,
            'schema': mock_schema,
            'model': mock_model,
        }


# --- BaseSettings (abstract) cannot be instantiated; we test subclasses ---

# --- SettingsWithCode tests (using IncomeSettings as concrete) ---
class TestSettingsWithCode:
    def test_init(self, mock_settings_deps):
        with patch('app.controllers.others.settings.SettingWithCodeFormUI'):
            inc = IncomeSettings()
            mock_settings_deps['load'].assert_called()
            assert inc.income is True
            assert inc.identifier is None

    def test_control_add_income(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.entery.text = MagicMock(return_value='Salary')
        inc.code.text = MagicMock(return_value='123')
        inc.manager = mock_settings_deps['model']
        with patch.object(inc, 'reset_enteries') as mock_reset, \
             patch.object(inc, 'show_data') as mock_show, \
             patch.object(inc, 'combo_manager') as mock_combo:
            inc.control(WorkingMode.ADD)
            mock_settings_deps['model'].create.assert_called()
            mock_reset.assert_called()
            mock_show.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.INCOME)

    def test_control_add_expense(self, mock_settings_deps):
        exp = ExpenseSettings()
        exp.entery.text = MagicMock(return_value='Rent')
        exp.code.text = MagicMock(return_value='456')
        exp.manager = mock_settings_deps['model']
        with patch.object(exp, 'reset_enteries') as mock_reset, \
             patch.object(exp, 'show_data') as mock_show, \
             patch.object(exp, 'combo_manager') as mock_combo:
            exp.control(WorkingMode.ADD)
            mock_settings_deps['model'].create.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.EXPENSES)

    def test_control_update(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.identifier = 1
        inc.entery.text = MagicMock(return_value='Salary')
        inc.code.text = MagicMock(return_value='123')
        inc.manager = mock_settings_deps['model']
        with patch.object(inc, 'reset_enteries') as mock_reset, \
             patch.object(inc, 'show_data') as mock_show:
            inc.control(WorkingMode.UPDATE)
            mock_settings_deps['model'].update.assert_called_with(1, mock_settings_deps['schema'].SETTINGS.return_value)
            mock_reset.assert_called()
            mock_show.assert_called()

    def test_control_validation_fail(self, mock_settings_deps):
        inc = IncomeSettings()
        entity = mock_settings_deps['schema'].SETTINGS.return_value
        entity.validate = MagicMock(return_value=False)
        inc.control(WorkingMode.ADD)
        mock_settings_deps['error'].assert_called_with("Verifier les données")

    def test_delete_success(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.identifier = 1
        inc.entery.text = MagicMock(return_value='Salary')
        inc.manager = mock_settings_deps['model']
        inc.check_used = MagicMock(return_value=False)
        with patch.object(inc, 'reset_enteries') as mock_reset:
            inc.delete()
            mock_settings_deps['model'].delete.assert_called_with(1)
            mock_reset.assert_called()
            assert inc.identifier is None

    def test_delete_used(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.identifier = 1
        inc.entery.text = MagicMock(return_value='Salary')
        inc.manager = mock_settings_deps['model']
        inc.check_used = MagicMock(return_value=True)
        inc.delete()
        mock_settings_deps['error'].assert_called_with("لا يمكن الحذف لأنه يتم إستعماله")
        mock_settings_deps['model'].delete.assert_not_called()

    def test_select_row(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.list = MagicMock()
        inc.list.currentRow = MagicMock(return_value=0)
        inc.list.item = MagicMock(side_effect=[
            MagicMock(text=MagicMock(return_value='1')),
            MagicMock(text=MagicMock(return_value='Salary')),
            MagicMock(text=MagicMock(return_value='123'))
        ])
        inc.entery.setText = MagicMock()
        inc.code.setValue = MagicMock()
        inc.select_row()
        assert inc.identifier == 1
        inc.entery.setText.assert_called_with('Salary')
        inc.code.setValue.assert_called_with(123)

    def test_show_data(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.list = MagicMock()
        inc.list.setItem = MagicMock()
        inc.nb = MagicMock()
        mock_data = [MagicMock(id=1, out_money='Rent', out_code=456)]
        mock_settings_deps['model'].get_by_filter.return_value = mock_data
        inc.manager = mock_settings_deps['model']
        inc.show_data({})
        inc.list.setItem.assert_called_with(0, 0, QTableWidgetItem(str(1)))
        inc.list.setItem.assert_any_call(0, 1, QTableWidgetItem('Rent'))
        inc.list.setItem.assert_any_call(0, 2, QTableWidgetItem(str(456)))
        assert inc.nb.setText.called_with('1')

    def test_reset_enteries(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.code.setValue = MagicMock()
        inc.entery.setText = MagicMock()
        inc.reset_enteries()
        inc.code.setValue.assert_called_with(0)
        inc.entery.setText.assert_called_with('')


# --- SettingsWithoutCode tests (using WaySettings as concrete) ---
class TestSettingsWithoutCode:
    def test_init(self, mock_settings_deps):
        with patch('app.controllers.others.settings.SettingFormUI'):
            way = WaySettings()
            mock_settings_deps['load'].assert_called()
            assert way.setting == ComboName.WAY_TEACHING  # from __init__

    def test_control_add(self, mock_settings_deps):
        way = WaySettings()
        way.entery.text = MagicMock(return_value='Online')
        way.manager = mock_settings_deps['model']
        with patch.object(way, 'reset_enteries') as mock_reset, \
             patch.object(way, 'show_data') as mock_show, \
             patch.object(way, 'combo_manager') as mock_combo:
            way.control(WorkingMode.ADD)
            mock_settings_deps['model'].create.assert_called()
            mock_reset.assert_called()
            mock_show.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.WAY_TEACHING)

    def test_control_update(self, mock_settings_deps):
        way = WaySettings()
        way.entery.text = MagicMock(return_value='Online')
        way.manager = mock_settings_deps['model']
        with patch.object(way, 'reset_enteries') as mock_reset, \
             patch.object(way, 'show_data') as mock_show, \
             patch.object(way, 'combo_manager') as mock_combo:
            way.control(WorkingMode.UPDATE)
            mock_settings_deps['model'].update_by_filter.assert_called()
            mock_reset.assert_called()
            mock_show.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.WAY_TEACHING)

    def test_control_invalid_setting(self, mock_settings_deps):
        # Force wrong setting
        with patch('app.controllers.others.settings.SettingsWithoutCode.__init__', lambda self, setting, parent: None):
            obj = SettingsWithoutCode.__new__(SettingsWithoutCode)
            obj.setting = 'invalid'
            obj.entery = MagicMock()
            obj.manager = mock_settings_deps['model']
            obj.control(WorkingMode.ADD)
            mock_settings_deps['error'].assert_called_with("Invalid setting type")

    def test_delete_success(self, mock_settings_deps):
        way = WaySettings()
        way.entery.text = MagicMock(return_value='Online')
        way.manager = mock_settings_deps['model']
        way.check_used = MagicMock(return_value=False)
        with patch.object(way, 'reset_enteries') as mock_reset, \
             patch.object(way, 'combo_manager') as mock_combo:
            way.delete()
            mock_settings_deps['model'].delete_by_filter.assert_called()
            mock_reset.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.WAY_TEACHING)

    def test_delete_used(self, mock_settings_deps):
        way = WaySettings()
        way.entery.text = MagicMock(return_value='Online')
        way.manager = mock_settings_deps['model']
        way.check_used = MagicMock(return_value=True)
        way.delete()
        mock_settings_deps['error'].assert_called_with("لا يمكن الحذف لأنه يتم إستعماله")
        mock_settings_deps['model'].delete_by_filter.assert_not_called()

    def test_way_select_row(self, mock_settings_deps):
        way = WaySettings()
        way.list = MagicMock()
        way.list.currentItem = MagicMock(return_value=MagicMock(text=MagicMock(return_value='Online')))
        way.entery.setText = MagicMock()
        way.way_select_row()
        way.entery.setText.assert_called_with('Online')

    def test_show_data(self, mock_settings_deps):
        way = WaySettings()
        way.list = MagicMock()
        way.list.addItem = MagicMock()
        way.nb = MagicMock()
        mock_data = [MagicMock(way_teaching='Online')]
        mock_settings_deps['model'].get_by_filter.return_value = mock_data
        way.manager = mock_settings_deps['model']
        way.setting = ComboName.WAY_TEACHING
        way.show_data({})
        way.list.addItem.assert_called_with('Online')
        assert way.nb.setText.called_with('1')


# --- Specific settings classes ---
class TestIncomeSettings:
    def test_check_used(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.check_used(123)
        mock_settings_deps['model'].check_used.assert_called_with(123)

    def test_show_data(self, mock_settings_deps):
        inc = IncomeSettings()
        inc.manager = mock_settings_deps['model']
        inc.show_data('Salary')
        mock_settings_deps['model'].get_filter.assert_called_with(entery='Salary')


class TestExpenseSettings:
    def test_check_used(self, mock_settings_deps):
        exp = ExpenseSettings()
        exp.check_used(456)
        mock_settings_deps['model'].check_used.assert_called_with(456)

    def test_show_data(self, mock_settings_deps):
        exp = ExpenseSettings()
        exp.manager = mock_settings_deps['model']
        exp.show_data('Rent')
        mock_settings_deps['model'].get_filter.assert_called_with(out_money='Rent')


class TestWaySettings:
    def test_check_used(self, mock_settings_deps):
        way = WaySettings()
        way.manager = mock_settings_deps['model']
        way.check_used('Online')
        mock_settings_deps['model'].get_filters.assert_called_with(way_teaching='Online')
        mock_settings_deps['model'].exists.assert_called()

    def test_show_data(self, mock_settings_deps):
        way = WaySettings()
        way.manager = mock_settings_deps['model']
        way.show_data('Online')
        mock_settings_deps['model'].get_filter.assert_called_with(way_teaching='Online')


class TestPaymentSettings:
    def test_check_used(self, mock_settings_deps):
        pay = PaymentSettings()
        pay.used_per_model = MagicMock(return_value=False)
        result = pay.check_used('Cash')
        assert result is False
        pay.used_per_model.assert_any_call('INCOME', 'Cash')
        pay.used_per_model.assert_any_call('EXPENSE', 'Cash')

    def test_used_per_model(self, mock_settings_deps):
        pay = PaymentSettings()
        pay.used_per_model('INCOME', 'Cash')
        mock_settings_deps['model'].get_filter.assert_called_with(way_payment='Cash')
        mock_settings_deps['model'].exists.assert_called()

    def test_payment_show(self, mock_settings_deps):
        pay = PaymentSettings()
        pay.manager = mock_settings_deps['model']
        pay.payment_show('Cash')
        mock_settings_deps['model'].get_filter.assert_called_with(way_payment='Cash')


class TestFournisseurSettings:
    def test_fournisseur_check_used(self, mock_settings_deps):
        fr = FournisseurSettings()
        fr.manager = mock_settings_deps['model']
        fr.fournisseur_check_used('Supplier')
        mock_settings_deps['model'].get_filters.assert_called_with(name='Supplier')
        mock_settings_deps['model'].exists.assert_called()

    def test_fournisseur_show(self, mock_settings_deps):
        fr = FournisseurSettings()
        fr.manager = mock_settings_deps['model']
        fr.fournisseur_show('Supplier')
        mock_settings_deps['model'].get_filter.assert_called_with(fr='Supplier')


# --- SettingsLogic tests ---
class TestSettingsLogic:
    def test_init(self, mock_settings_deps):
        with patch('app.controllers.others.settings.SettingsUI'):
            logic = SettingsLogic()
            mock_settings_deps['load'].assert_called()
            assert hasattr(logic, 'plane')
            # Check that settings were added
            assert logic.plane.addWidget.call_count == 5

    def test_setup(self, mock_settings_deps):
        logic = SettingsLogic()
        # The setup is called in __init__, but we can test buttons
        assert hasattr(logic.way_btn, 'clicked')