# test_controllers.py
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate

# Import the classes to test (they will be patched with mocks for UI)
from app.controllers.classes.classes import ClassesLogic, ClasseleveLogic, ClassPart
from app.controllers.finance.balance import BalanceLogic
from app.controllers.finance.expenses import OutMoneyLogic
from app.controllers.finance.income import EnteryLogic
from app.controllers.finance.transfer import TransferLogic
from app.controllers.finance import MoneyPart
from app.utils import WorkingMode, ReportType, Account


# ---------- Fixtures and mocks ----------
@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock all external dependencies to avoid real UI and DB."""
    with patch('app.controllers.classes.classes.load_gui') as mock_load_gui, \
         patch('app.controllers.classes.classes.get_model') as mock_get_model, \
         patch('app.controllers.classes.classes.get_combo_manager') as mock_combo_manager, \
         patch('app.controllers.classes.classes.create_table_model') as mock_create_table, \
         patch('app.controllers.classes.classes.create_popup_factory') as mock_popup_factory, \
         patch('app.controllers.classes.classes.SchemaFactory') as mock_schema_factory, \
         patch('app.controllers.classes.classes.get_username', return_value='test_user'), \
         patch('app.controllers.classes.classes.error') as mock_error, \
         patch('app.controllers.classes.classes.get_student_list') as mock_student_list, \
         patch('app.controllers.finance.balance.load_gui') as mock_balance_load, \
         patch('app.controllers.finance.balance.get_model') as mock_balance_get_model, \
         patch('app.controllers.finance.balance.get_combo_manager') as mock_balance_combo, \
         patch('app.controllers.finance.balance.create_table_model') as mock_balance_table, \
         patch('app.controllers.finance.expenses.load_gui') as mock_exp_load, \
         patch('app.controllers.finance.expenses.get_model') as mock_exp_get_model, \
         patch('app.controllers.finance.expenses.get_combo_manager') as mock_exp_combo, \
         patch('app.controllers.finance.expenses.create_table_model') as mock_exp_table, \
         patch('app.controllers.finance.expenses.create_popup_factory') as mock_exp_popup, \
         patch('app.controllers.finance.expenses.SchemaFactory') as mock_exp_schema, \
         patch('app.controllers.finance.expenses.get_username', return_value='test_user'), \
         patch('app.controllers.finance.income.load_gui') as mock_inc_load, \
         patch('app.controllers.finance.income.get_model') as mock_inc_get_model, \
         patch('app.controllers.finance.income.get_combo_manager') as mock_inc_combo, \
         patch('app.controllers.finance.income.create_table_model') as mock_inc_table, \
         patch('app.controllers.finance.income.create_popup_factory') as mock_inc_popup, \
         patch('app.controllers.finance.income.SchemaFactory') as mock_inc_schema, \
         patch('app.controllers.finance.income.get_username', return_value='test_user'), \
         patch('app.controllers.finance.transfer.load_gui') as mock_trans_load, \
         patch('app.controllers.finance.transfer.get_model') as mock_trans_get_model, \
         patch('app.controllers.finance.transfer.get_combo_manager') as mock_trans_combo, \
         patch('app.controllers.finance.transfer.create_table_model') as mock_trans_table, \
         patch('app.controllers.finance.transfer.SchemaFactory') as mock_trans_schema, \
         patch('app.controllers.finance.transfer.get_username', return_value='test_user'), \
         patch('app.controllers.finance.__init__.load_gui') as mock_part_load, \
         patch('app.controllers.classes.__init__.load_gui') as mock_classpart_load:
        
        # Provide mocks for common objects
        mock_combo_mgr = MagicMock()
        mock_combo_mgr.update_combo = MagicMock()
        mock_combo_mgr.update_cache_from_db = MagicMock()
        mock_combo_mgr.get_cached_data = MagicMock(return_value=[('Class A',), ('Class B',)])
        
        mock_model = MagicMock()
        mock_model.get_by_id = MagicMock(return_value=MagicMock(__dict__={'id':1, 'name':'Test'}))
        mock_model.create = MagicMock()
        mock_model.update = MagicMock()
        mock_model.delete = MagicMock()
        mock_model.get_data_using_filters = MagicMock(return_value=MagicMock())
        mock_model.get_by_filter = MagicMock(return_value=[MagicMock()])
        mock_model.get_total = MagicMock(return_value=100)
        mock_model.get_balance = MagicMock(return_value=50)
        mock_model.set_dynamic_metadata = MagicMock()
        mock_model.export_data = MagicMock()
        mock_model.get_filters = MagicMock(return_value={})
        mock_model.exists = MagicMock(return_value=False)
        mock_model.get_code = MagicMock(return_value=123)
        mock_model.get_type = MagicMock(return_value='Type')
        mock_model.sup_security = MagicMock()
        mock_model.check = MagicMock(return_value=True)
        mock_model.get_current_data = MagicMock(return_value=[])

        def get_model_side_effect(name):
            if name in ['CLASSES', 'ENROLLMENT', 'EXPENSES', 'INCOME', 'BALANCE', 'TRANSFER', 'SETTINGS']:
                return mock_model
            return MagicMock()

        mock_get_model.side_effect = get_model_side_effect
        mock_balance_get_model.side_effect = get_model_side_effect
        mock_exp_get_model.side_effect = get_model_side_effect
        mock_inc_get_model.side_effect = get_model_side_effect
        mock_trans_get_model.side_effect = get_model_side_effect

        # Table model mock
        mock_table_model = MagicMock()
        mock_table_model.ID_COLUMN = 0
        mock_table_model.rowCount = MagicMock(return_value=5)
        mock_table_model.data = MagicMock(return_value=42)
        mock_table_model.get_current_data = MagicMock(return_value=[])
        mock_table_model.refresh = MagicMock()
        mock_table_model.total_price = 200
        mock_table_model.setData = MagicMock()

        mock_create_table.return_value = mock_table_model
        mock_balance_table.return_value = mock_table_model
        mock_exp_table.return_value = mock_table_model
        mock_inc_table.return_value = mock_table_model
        mock_trans_table.return_value = mock_table_model

        # Popup factory mock
        mock_dialog = MagicMock()
        mock_dialog.content = MagicMock()
        mock_dialog.content.get_data = MagicMock(return_value={'name':'Test', 'way':'Cash', 'teacher':'Mr. X', 'note':'', 'price':100, 'date':'2026-01-01', 'bill_num':'123', 'type':'Type', 'cheq_num':'', 'code':456, 'in_bank':'البنك', 'bill_number':'', 'code_input':789})
        mock_dialog.content.repopulate_fields = MagicMock()
        mock_dialog.confirmed = MagicMock()
        mock_dialog.show = MagicMock()
        mock_popup_factory.return_value = mock_dialog
        mock_exp_popup.return_value = mock_dialog
        mock_inc_popup.return_value = mock_dialog

        # Schema factory mock
        mock_entity = MagicMock()
        mock_entity.validate = MagicMock(return_value=True)
        mock_schema_factory.CLASSES.return_value = mock_entity
        mock_schema_factory.ENROLLMENT.return_value = mock_entity
        mock_exp_schema.EXPENSES.return_value = mock_entity
        mock_inc_schema.INCOME.return_value = mock_entity
        mock_trans_schema.TRANSFER.return_value = mock_entity

        # Student list mock
        mock_student_list.return_value = [MagicMock()]

        # Error mock
        mock_error.side_effect = lambda msg: print(f"Error: {msg}")  # For test output

        # QMessageBox mock
        with patch('app.controllers.classes.classes.QMessageBox') as mock_qmsg:
            mock_qmsg_instance = MagicMock()
            mock_qmsg_instance.question = MagicMock(return_value=QMessageBox.StandardButton.Yes)
            mock_qmsg.return_value = mock_qmsg_instance

            yield {
                'load_gui': mock_load_gui,
                'get_model': mock_get_model,
                'combo_manager': mock_combo_mgr,
                'table_model': mock_table_model,
                'popup_factory': mock_popup_factory,
                'schema_factory': mock_schema_factory,
                'error': mock_error,
                'student_list': mock_student_list,
                'qmsg': mock_qmsg,
                'model': mock_model,
            }

