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


# ---------- Tests for ClassesLogic ----------
class TestClassesLogic:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.classes.classes.ClassesUI'):
            logic = ClassesLogic()
            assert logic.model is not None
            assert logic.identifier == 0
            mock_dependencies['load_gui'].assert_called_once()

    def test_set_table(self, mock_dependencies):
        logic = ClassesLogic()
        logic.set_table()
        mock_dependencies['table_model'].assert_called()
        assert logic.class_table.model() is not None

    def test_setup(self, mock_dependencies):
        logic = ClassesLogic()
        logic.setup()
        # Check signals connected (we can't easily test, but we can assert that buttons exist)
        assert hasattr(logic.add_btn, 'clicked')

    def test_aquire_data_add(self, mock_dependencies):
        logic = ClassesLogic()
        logic.aquire_data(WorkingMode.ADD)
        mock_dependencies['popup_factory'].assert_called_with(
            kind='CLASS_FORM', title="إضافة قسم", parent=logic
        )
        # Trigger confirm
        dialog = mock_dependencies['popup_factory'].return_value
        # Simulate confirm signal
        dialog.confirmed.emit()
        # control should be called; we mock it
        with patch.object(logic, 'control') as mock_control:
            dialog.confirmed.emit()
            mock_control.assert_called()

    def test_aquire_data_update_no_identifier(self, mock_dependencies):
        logic = ClassesLogic()
        logic.identifier = None
        logic.aquire_data(WorkingMode.UPDATE)
        mock_dependencies['error'].assert_called_with("يرجى تحديد قسم")

    def test_aquire_data_update_with_identifier(self, mock_dependencies):
        logic = ClassesLogic()
        logic.identifier = 1
        logic.aquire_data(WorkingMode.UPDATE)
        mock_dependencies['popup_factory'].assert_called()
        mock_dependencies['model'].get_by_id.assert_called_with(1)

    def test_control_add_success(self, mock_dependencies):
        logic = ClassesLogic()
        logic.manager = mock_dependencies['model']
        data = {'name':'A', 'way':'B', 'teacher':'C', 'note':'', 'price':100}
        logic.control(WorkingMode.ADD, data)
        mock_dependencies['model'].create.assert_called()
        mock_dependencies['combo_manager'].update_cache_from_db.assert_called_with(combo_name='CLASS')

    def test_control_update_success(self, mock_dependencies):
        logic = ClassesLogic()
        logic.identifier = 1
        logic.manager = mock_dependencies['model']
        data = {'name':'A', 'way':'B', 'teacher':'C', 'note':'', 'price':100}
        logic.control(WorkingMode.UPDATE, data)
        mock_dependencies['model'].update.assert_called_with(1, mock_dependencies['schema_factory'].CLASSES.return_value)

    def test_control_validation_fail(self, mock_dependencies):
        logic = ClassesLogic()
        entity = mock_dependencies['schema_factory'].CLASSES.return_value
        entity.validate = MagicMock(return_value=False)
        data = {}
        logic.control(WorkingMode.ADD, data)
        mock_dependencies['error'].assert_called_with("الرجاء ملء جميع الحقول")

    def test_select_row(self, mock_dependencies):
        logic = ClassesLogic()
        logic.model = mock_dependencies['table_model']
        # Mock selection model
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = [MagicMock(row=MagicMock(return_value=0))]
        logic.class_table.selectionModel = MagicMock(return_value=mock_selection)
        logic.select_row()
        assert logic.identifier == 42

    def test_select_row_no_selection(self, mock_dependencies):
        logic = ClassesLogic()
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = []
        logic.class_table.selectionModel = MagicMock(return_value=mock_selection)
        logic.select_row()
        mock_dependencies['error'].assert_called_with("يرجى تحديد قسم")

    def test_delete_class(self, mock_dependencies):
        logic = ClassesLogic()
        logic.identifier = 1
        logic.delete_class()
        mock_dependencies['model'].sup_security.assert_called_with(1)
        mock_dependencies['combo_manager'].update_cache_from_db.assert_called_with("classes")

    def test_show_class(self, mock_dependencies):
        logic = ClassesLogic()
        logic.search.text = MagicMock(return_value='Class')
        logic.teacher_search.currentText = MagicMock(return_value='Teacher')
        logic.manager = mock_dependencies['model']
        logic.show_class()
        mock_dependencies['model'].get_data_using_filters.assert_called_with(name='Class', teacher='Teacher')
        mock_dependencies['model'].get_by_filter.assert_called()
        mock_dependencies['table_model'].refresh.assert_called()
        assert logic.nb.text() == '5'  # rowCount returns 5

    def test_populate_combos(self, mock_dependencies):
        logic = ClassesLogic()
        logic.populate_combos()
        mock_dependencies['combo_manager'].update_combo.assert_called_with(logic.teacher_search, 'TEACHER')

    def test_export(self, mock_dependencies):
        logic = ClassesLogic()
        logic.model = mock_dependencies['table_model']
        logic.model.get_current_data = MagicMock(return_value=[MagicMock()])
        logic.model.rowCount = MagicMock(return_value=10)
        logic.manager = mock_dependencies['model']
        logic.export(ReportType.PRINT)
        mock_dependencies['model'].set_dynamic_metadata.assert_called()
        mock_dependencies['model'].export_data.assert_called_with(report_type=ReportType.PRINT, parent=logic)


# ---------- Tests for ClasseleveLogic ----------
class TestClasseleveLogic:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.classes.classes.ClasseleveUI'):
            logic = ClasseleveLogic()
            assert logic.model is not None
            assert logic.model_classeleve is not None

    def test_setup(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.setup()
        # Check signals connected

    def test_get_student_id_success(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.model = mock_dependencies['table_model']
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = [MagicMock(row=MagicMock(return_value=0))]
        logic.student_search_list.selectionModel = MagicMock(return_value=mock_selection)
        assert logic.get_student_id() == 42

    def test_get_student_id_fail(self, mock_dependencies):
        logic = ClasseleveLogic()
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = []
        logic.student_search_list.selectionModel = MagicMock(return_value=mock_selection)
        logic.get_student_id()
        mock_dependencies['error'].assert_called_with("يرجى تحديد التلميذ")

    def test_add_success(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.classes.currentText = MagicMock(return_value='Class A')
        logic.get_student_id = MagicMock(return_value=1)
        logic.manager = mock_dependencies['model']
        logic.manager.check = MagicMock(return_value=True)
        logic.add()
        mock_dependencies['model'].create.assert_called()

    def test_add_no_class(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.classes.currentText = MagicMock(return_value='')
        logic.add()
        mock_dependencies['error'].assert_called_with("يرجى اختيار صف")

    def test_add_student_already_in_class(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.classes.currentText = MagicMock(return_value='Class A')
        logic.get_student_id = MagicMock(return_value=1)
        logic.manager = mock_dependencies['model']
        logic.manager.check = MagicMock(return_value=False)
        logic.add()
        mock_dependencies['error'].assert_called_with("هذا التلميذ موجود في هذا الصف")

    def test_sup_security_yes(self, mock_dependencies):
        logic = ClasseleveLogic()
        with patch('app.controllers.classes.classes.QMessageBox') as mock_qmsg:
            mock_qmsg_instance = MagicMock()
            mock_qmsg_instance.question = MagicMock(return_value=QMessageBox.StandardButton.Yes)
            mock_qmsg.return_value = mock_qmsg_instance
            logic.line_to_delete = MagicMock(return_value=1)
            logic.manager = mock_dependencies['model']
            logic.sup_security()
            mock_dependencies['model'].delete.assert_called_with(1)
            mock_dependencies['table_model'].refresh.assert_called()

    def test_sup_security_no(self, mock_dependencies):
        logic = ClasseleveLogic()
        with patch('app.controllers.classes.classes.QMessageBox') as mock_qmsg:
            mock_qmsg_instance = MagicMock()
            mock_qmsg_instance.question = MagicMock(return_value=QMessageBox.StandardButton.No)
            mock_qmsg.return_value = mock_qmsg_instance
            logic.sup_security()
            mock_dependencies['model'].delete.assert_not_called()

    def test_line_to_delete(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.model_classeleve = mock_dependencies['table_model']
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = [MagicMock(row=MagicMock(return_value=0))]
        logic.students.selectionModel = MagicMock(return_value=mock_selection)
        assert logic.line_to_delete() == 42

    def test_show_classeleve(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.student_search.text = MagicMock(return_value='')
        logic.classes.currentText = MagicMock(return_value='Class A')
        logic.manager = mock_dependencies['model']
        logic.show_classeleve()
        mock_dependencies['model'].get_filters.assert_called_with(class_name='Class A')
        mock_dependencies['model'].get_by_filter.assert_called()

    def test_show_students_list(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.show_students_list('test')
        mock_dependencies['student_list'].assert_called_with('test')
        mock_dependencies['table_model'].refresh.assert_called()

    def test_reset(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.classes.setCurrentIndex = MagicMock()
        logic.reset()
        logic.classes.setCurrentIndex.assert_called_with(-1)

    def test_populate_combo(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.populate_combo()
        mock_dependencies['combo_manager'].get_cached_data.assert_called_with(data_name='CLASS')
        assert logic.classes.addItem.called

    def test_export(self, mock_dependencies):
        logic = ClasseleveLogic()
        logic.model_classeleve = mock_dependencies['table_model']
        logic.model_classeleve.get_current_data = MagicMock(return_value=[])
        logic.model_classeleve.rowCount = MagicMock(return_value=5)
        logic.classes.currentText = MagicMock(return_value='Class A')
        logic.manager = mock_dependencies['model']
        logic.export(ReportType.PRINT)
        mock_dependencies['model'].set_dynamic_metadata.assert_called_with(data_to_export=[], row_count=5, class_name='Class A')
        mock_dependencies['model'].export_data.assert_called_with(report_type=ReportType.PRINT, parent=logic)


# ---------- Tests for ClassPart ----------
class TestClassPart:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.classes.__init__.ClassPartUI'):
            part = ClassPart()
            mock_dependencies['load_gui'].assert_called()
            assert part.stackedWidget.count() == 2

    def test_setup(self, mock_dependencies):
        part = ClassPart()
        part.setup()
        # Check signals

    def test_go_to_classes(self, mock_dependencies):
        part = ClassPart()
        part.c = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.classes = MagicMock()
        part.go_to_classes()
        part.stackedWidget.setCurrentIndex.assert_called_with(0)
        part.c.populate_combos.assert_called()
        part.buttons.assert_called_with(part.classes)

    def test_go_to_classeleve(self, mock_dependencies):
        part = ClassPart()
        part.ce = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.classeleve = MagicMock()
        part.go_to_classeleve()
        part.stackedWidget.setCurrentIndex.assert_called_with(1)
        part.ce.populate_combo.assert_called()
        part.buttons.assert_called_with(part.classeleve)

    def test_buttons(self, mock_dependencies):
        part = ClassPart()
        part.classes = MagicMock()
        part.classeleve = MagicMock()
        button = MagicMock()
        part.buttons(button)
        part.classes.setStyleSheet.assert_called_with("color: white")
        part.classeleve.setStyleSheet.assert_called_with("color: white")
        button.setStyleSheet.assert_called_with("color: green")


# ---------- Tests for BalanceLogic ----------
class TestBalanceLogic:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.finance.balance.BalanceUI'):
            logic = BalanceLogic()
            mock_dependencies['load_gui'].assert_called()
            assert logic.model is not None
            mock_dependencies['model'].get_balance.assert_called()  # called in set_totals

    def test_setup(self, mock_dependencies):
        logic = BalanceLogic()
        logic.setup()
        # signals

    def test_setup_table(self, mock_dependencies):
        logic = BalanceLogic()
        logic.setup_table()
        mock_dependencies['table_model'].assert_called()
        assert logic.tbl.model() is not None
        logic.set_totals.assert_called()  # called inside

    def test_populate_combo(self, mock_dependencies):
        logic = BalanceLogic()
        logic.populate_combo()
        mock_dependencies['combo_manager'].update_combo.assert_called_with(logic.way, 'WAY_PAYMENT')

    def test_show_table(self, mock_dependencies):
        logic = BalanceLogic()
        logic.operatore.currentText = MagicMock(return_value='op')
        logic.price_input.value = MagicMock(return_value=0)
        logic.du.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-01')))
        logic.to.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-02')))
        logic.way.currentText = MagicMock(return_value='Cash')
        logic.manager = mock_dependencies['model']
        logic.show_table()
        mock_dependencies['model'].get_balance.assert_called_with(
            way_payment='Cash', from_date='2026-01-01', to_date='2026-01-02', price=None, operator='op'
        )
        mock_dependencies['table_model'].refresh.assert_called()

    def test_set_totals(self, mock_dependencies):
        logic = BalanceLogic()
        logic.expenses_manager = mock_dependencies['model']
        logic.income_manager = mock_dependencies['model']
        logic.manager = mock_dependencies['model']
        logic.set_totals()
        assert logic.total_out.text() == '100'
        assert logic.total_in.text() == '100'
        assert logic.solde.text() == '50'

    def test_reset(self, mock_dependencies):
        logic = BalanceLogic()
        logic.operatore.setCurrentIndex = MagicMock()
        logic.price_input.setValue = MagicMock()
        logic.du.setDate = MagicMock()
        logic.to.setDate = MagicMock()
        logic.way.setCurrentIndex = MagicMock()
        logic.reset()
        logic.operatore.setCurrentIndex.assert_called_with(-1)
        logic.price_input.setValue.assert_called_with(0)
        logic.du.setDate.assert_called()
        logic.to.setDate.assert_called()

    def test_export(self, mock_dependencies):
        logic = BalanceLogic()
        logic.model = mock_dependencies['table_model']
        logic.model.get_current_data = MagicMock(return_value=[])
        logic.income_manager = mock_dependencies['model']
        logic.expenses_manager = mock_dependencies['model']
        logic.manager = mock_dependencies['model']
        logic.export(ReportType.PRINT)
        mock_dependencies['model'].set_dynamic_metadata.assert_called()
        mock_dependencies['model'].export_data.assert_called_with(report_type=ReportType.PRINT, parent=logic)


# ---------- Tests for OutMoneyLogic ----------
class TestOutMoneyLogic:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.finance.expenses.OutMoneyUI'):
            logic = OutMoneyLogic()
            mock_dependencies['load_gui'].assert_called()
            assert logic.model is not None

    def test_setup(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.setup()

    def test_setup_table(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.setup_table()
        mock_dependencies['table_model'].assert_called()
        assert logic.tbl.model() is not None
        assert logic.total.text() == '100'

    def test_aquire_data_add(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.aquire_data(WorkingMode.ADD)
        mock_dependencies['popup_factory'].assert_called_with(kind='EXPENSES', title="إضافة مصروف", parent=logic)
        # Trigger confirm
        dialog = mock_dependencies['popup_factory'].return_value
        with patch.object(logic, 'control') as mock_control:
            dialog.confirmed.emit()
            mock_control.assert_called()

    def test_aquire_data_update(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.identifier = 1
        logic.aquire_data(WorkingMode.UPDATE)
        mock_dependencies['model'].get_by_id.assert_called_with(1)
        dialog = mock_dependencies['popup_factory'].return_value
        dialog.content.repopulate_fields.assert_called()

    def test_control_add_success(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.manager = mock_dependencies['model']
        logic.unique = MagicMock(return_value=False)
        data = {'name':'A','bill_num':'123','date':'2026-01-01','type':'T','way':'Cash','cheq_num':'','price':100,'note':'','code':456,'in_bank':'البنك'}
        logic.control(WorkingMode.ADD, data)
        mock_dependencies['model'].create.assert_called()

    def test_control_add_duplicate(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.manager = mock_dependencies['model']
        logic.unique = MagicMock(return_value=True)
        data = {'bill_num':'123','date':'2026-01-01'}
        logic.control(WorkingMode.ADD, data)
        mock_dependencies['error'].assert_called_with("هذا المصروف موجود")

    def test_control_update(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.identifier = 1
        logic.manager = mock_dependencies['model']
        data = {'name':'A','bill_num':'123','date':'2026-01-01','type':'T','way':'Cash','cheq_num':'','price':100,'note':'','code':456,'in_bank':'البنك'}
        logic.control(WorkingMode.UPDATE, data)
        mock_dependencies['model'].update.assert_called_with(1, mock_dependencies['schema_factory'].EXPENSES.return_value)

    def test_delete(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.identifier = 1
        logic.delete()
        mock_dependencies['model'].delete.assert_called_with(1)

    def test_reset_filter(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.operatore.setCurrentIndex = MagicMock()
        logic.price_search.setValue = MagicMock()
        logic.way_search.setCurrentIndex = MagicMock()
        logic.du.setDate = MagicMock()
        logic.to.setDate = MagicMock()
        logic.type_search.setCurrentIndex = MagicMock()
        logic.name_search.setCurrentIndex = MagicMock()
        logic.reset_filter()
        # assertions

    def test_show_out(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.name_search.currentText = MagicMock(return_value='Name')
        logic.way_search.currentText = MagicMock(return_value='Cash')
        logic.type_search.currentText = MagicMock(return_value='Type')
        logic.du.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-01')))
        logic.to.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-02')))
        logic.price_search.value = MagicMock(return_value=0)
        logic.operatore.currentText = MagicMock(return_value='op')
        logic.code.value = MagicMock(return_value=0)
        logic.manager = mock_dependencies['model']
        logic.show_out()
        mock_dependencies['model'].get_filters.assert_called()
        mock_dependencies['model'].get_by_filter.assert_called()
        mock_dependencies['table_model'].refresh.assert_called()
        assert logic.total.text() == '100'

    def test_populate_combo(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.populate_combo()
        mock_dependencies['combo_manager'].update_combo.assert_any_call(logic.name_search, 'FR')
        mock_dependencies['combo_manager'].update_combo.assert_any_call(logic.type_search, 'EXPENSES')
        mock_dependencies['combo_manager'].update_combo.assert_any_call(logic.way_search, 'WAY_PAYMENT')

    def test_select_out(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.model = mock_dependencies['table_model']
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = [MagicMock(row=MagicMock(return_value=0))]
        logic.tbl.selectionModel = MagicMock(return_value=mock_selection)
        with patch.object(logic, 'aquire_data') as mock_aquire:
            logic.select_out()
            assert logic.identifier == 42
            mock_aquire.assert_called_with("update")

    def test_select_out_no_selection(self, mock_dependencies):
        logic = OutMoneyLogic()
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = []
        logic.tbl.selectionModel = MagicMock(return_value=mock_selection)
        logic.select_out()
        mock_dependencies['error'].assert_called_with("يرجى تحديد المصروف")

    def test_unique(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.manager = mock_dependencies['model']
        logic.unique('123', '2026-01-01')
        mock_dependencies['model'].get_filters.assert_called_with(bill_num='123', from_date='2026-01-01', to_date='2026-01-01')
        mock_dependencies['model'].exists.assert_called()

    def test_get_code(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.settings_manager = mock_dependencies['model']
        logic.type_search.currentText = MagicMock(return_value='Type')
        logic.get_code()
        mock_dependencies['model'].get_code.assert_called_with(income=None, expense='Type')
        assert logic.code.setValue.called

    def test_get_type(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.settings_manager = mock_dependencies['model']
        logic.code.value = MagicMock(return_value=123)
        logic.get_type()
        mock_dependencies['model'].get_type.assert_called_with(income_code=None, expense_code=123)
        logic.type_search.setCurrentText.assert_called()

    def test_export(self, mock_dependencies):
        logic = OutMoneyLogic()
        logic.model = mock_dependencies['table_model']
        logic.model.get_current_data = MagicMock(return_value=[MagicMock(price=10), MagicMock(price=20)])
        logic.manager = mock_dependencies['model']
        logic.export(ReportType.PRINT)
        mock_dependencies['model'].set_dynamic_metadata.assert_called_with(total_price=30, data_to_export=[MagicMock(), MagicMock()])
        mock_dependencies['model'].export_data.assert_called_with(report_type=ReportType.PRINT, parent=logic)

    def test_get_total(self, mock_dependencies):
        logic = OutMoneyLogic()
        data = [MagicMock(price=10), MagicMock(price=20)]
        assert logic.get_total(data) == 30


# ---------- Tests for EnteryLogic ----------
class TestEnteryLogic:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.finance.income.EnteryMoneyUI'):
            logic = EnteryLogic()
            mock_dependencies['load_gui'].assert_called()
            assert logic.model is not None

    def test_setup(self, mock_dependencies):
        logic = EnteryLogic()
        logic.setup()

    def test_setup_table(self, mock_dependencies):
        logic = EnteryLogic()
        logic.setup_table()
        mock_dependencies['table_model'].assert_called()
        assert logic.tbl.model() is not None
        assert logic.total.text() == '200'  # total_price from mock

    def test_aquire_data_add(self, mock_dependencies):
        logic = EnteryLogic()
        logic.aquire_data(WorkingMode.ADD)
        mock_dependencies['popup_factory'].assert_called_with(kind='INCOME', title="إضافة دخل", parent=logic)

    def test_aquire_data_update(self, mock_dependencies):
        logic = EnteryLogic()
        logic.identifier = 1
        logic.aquire_data(WorkingMode.UPDATE)
        mock_dependencies['model'].get_by_id.assert_called_with(1)
        dialog = mock_dependencies['popup_factory'].return_value
        dialog.content.repopulate_fields.assert_called()

    def test_control_add(self, mock_dependencies):
        logic = EnteryLogic()
        logic.manager = mock_dependencies['model']
        data = {'name':'A','date':'2026-01-01','type':'T','way':'Cash','price':100,'note':'','bill_number':'123','cheq_num':'','code_input':456,'in_bank':'البنك'}
        logic.control(WorkingMode.ADD, data)
        mock_dependencies['model'].create.assert_called()

    def test_control_update(self, mock_dependencies):
        logic = EnteryLogic()
        logic.identifier = 1
        logic.manager = mock_dependencies['model']
        data = {'name':'A','date':'2026-01-01','type':'T','way':'Cash','price':100,'note':'','bill_number':'123','cheq_num':'','code_input':456,'in_bank':'البنك'}
        logic.control(WorkingMode.UPDATE, data)
        mock_dependencies['model'].update.assert_called_with(1, mock_dependencies['schema_factory'].INCOME.return_value)

    def test_select(self, mock_dependencies):
        logic = EnteryLogic()
        logic.model = mock_dependencies['table_model']
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = [MagicMock(row=MagicMock(return_value=0))]
        logic.tbl.selectionModel = MagicMock(return_value=mock_selection)
        # Mock data: first column id, fifth column type
        logic.model.data = MagicMock(side_effect=[42, 'تسجيل'])  # first call id, second call type
        logic.select()
        assert logic.identifier == 42
        mock_dependencies['error'].assert_called_with("لا يمكن التحديث")

    def test_select_no_selection(self, mock_dependencies):
        logic = EnteryLogic()
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = []
        logic.tbl.selectionModel = MagicMock(return_value=mock_selection)
        logic.select()
        mock_dependencies['error'].assert_called_with("يرجى تحديد التلميذ")

    def test_delete_income(self, mock_dependencies):
        logic = EnteryLogic()
        logic.identifier = 1
        logic.delete_income()
        mock_dependencies['model'].delete.assert_called_with(1)

    def test_delete_income_no_id(self, mock_dependencies):
        logic = EnteryLogic()
        logic.identifier = None
        logic.delete_income()
        mock_dependencies['error'].assert_called_with("يرجى تحديد الدخل")

    def test_reset_filter(self, mock_dependencies):
        logic = EnteryLogic()
        logic.operatore.setCurrentIndex = MagicMock()
        logic.price_search.setValue = MagicMock()
        logic.way_search.setCurrentIndex = MagicMock()
        logic.type_search.setCurrentIndex = MagicMock()
        logic.to.setDate = MagicMock()
        logic.du.setDate = MagicMock()
        logic.code.setValue = MagicMock()
        logic.name_search.setText = MagicMock()
        logic.reset_filter()
        # assertions

    def test_show_entery(self, mock_dependencies):
        logic = EnteryLogic()
        logic.name_search.text = MagicMock(return_value='Name')
        logic.way_search.currentText = MagicMock(return_value='Cash')
        logic.type_search.currentText = MagicMock(return_value='Type')
        logic.du.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-01')))
        logic.to.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-02')))
        logic.price_search.value = MagicMock(return_value=0)
        logic.operatore.currentText = MagicMock(return_value='op')
        logic.code.value = MagicMock(return_value=0)
        logic.manager = mock_dependencies['model']
        logic.show_entery()
        mock_dependencies['model'].get_filter.assert_called()
        mock_dependencies['table_model'].refresh.assert_called()
        assert logic.total.text() == '100'

    def test_populate_combo(self, mock_dependencies):
        logic = EnteryLogic()
        logic.populate_combo()
        mock_dependencies['combo_manager'].update_combo.assert_any_call(logic.type_search, 'INCOME')
        mock_dependencies['combo_manager'].update_combo.assert_any_call(logic.way_search, 'WAY_PAYMENT')

    def test_get_code(self, mock_dependencies):
        logic = EnteryLogic()
        logic.settings_manager = mock_dependencies['model']
        logic.type_search.currentText = MagicMock(return_value='Type')
        logic.get_code()
        mock_dependencies['model'].get_code.assert_called_with(income='Type', expense=None)
        logic.code.setValue.assert_called_with(123)

    def test_get_type(self, mock_dependencies):
        logic = EnteryLogic()
        logic.settings_manager = mock_dependencies['model']
        logic.code.value = MagicMock(return_value=123)
        logic.get_type()
        mock_dependencies['model'].get_type.assert_called_with(income_code=123, expense_code=None)
        logic.type_search.setCurrentText.assert_called()

    def test_export(self, mock_dependencies):
        logic = EnteryLogic()
        logic.model = mock_dependencies['table_model']
        logic.model.get_current_data = MagicMock(return_value=[MagicMock(price=10), MagicMock(price=20)])
        logic.manager = mock_dependencies['model']
        logic.export(ReportType.PRINT)
        mock_dependencies['model'].set_dynamic_metadata.assert_called_with(30, [MagicMock(), MagicMock()])
        mock_dependencies['model'].export_data.assert_called_with(report_type=ReportType.PRINT, parent=logic)

    def test_get_total(self, mock_dependencies):
        logic = EnteryLogic()
        data = [MagicMock(price=10), MagicMock(price=20)]
        assert logic.get_total(data) == 30


# ---------- Tests for MoneyPart ----------
class TestMoneyPart:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.finance.__init__.MoneyUI'):
            part = MoneyPart()
            mock_dependencies['load_gui'].assert_called()
            assert part.stackedWidget.count() == 4

    def test_setup(self, mock_dependencies):
        part = MoneyPart()
        part.setup()

    def test_income(self, mock_dependencies):
        part = MoneyPart()
        part.e = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.add_money = MagicMock()
        part.income()
        part.e.setup_table.assert_called()
        part.e.populate_combo.assert_called()
        part.buttons.assert_called_with(part.add_money)

    def test_expenses(self, mock_dependencies):
        part = MoneyPart()
        part.o = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.out_money = MagicMock()
        part.expenses()
        part.o.setup_table.assert_called()
        part.o.populate_combo.assert_called()
        part.buttons.assert_called_with(part.out_money)

    def test_balance(self, mock_dependencies):
        part = MoneyPart()
        part.s = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.solde = MagicMock()
        part.balance()
        part.s.setup_table.assert_called()
        part.s.populate_combo.assert_called()
        part.buttons.assert_called_with(part.solde)

    def test_go_to_transfer(self, mock_dependencies):
        part = MoneyPart()
        part.t = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.transfer = MagicMock()
        part.go_to_transfer()
        part.t.setup_table.assert_called()
        part.buttons.assert_called_with(part.transfer)

    def test_buttons(self, mock_dependencies):
        part = MoneyPart()
        part.add_money = MagicMock()
        part.out_money = MagicMock()
        part.solde = MagicMock()
        part.transfer = MagicMock()
        button = MagicMock()
        part.buttons(button)
        part.add_money.setStyleSheet.assert_called_with("color: white")
        part.out_money.setStyleSheet.assert_called_with("color: white")
        part.solde.setStyleSheet.assert_called_with("color: white")
        part.transfer.setStyleSheet.assert_called_with("color: white")
        button.setStyleSheet.assert_called_with("color: green")


# ---------- Tests for TransferLogic ----------
class TestTransferLogic:
    def test_init(self, mock_dependencies):
        with patch('app.controllers.finance.transfer.TransferUI'):
            logic = TransferLogic()
            mock_dependencies['load_gui'].assert_called()
            assert logic.model is not None

    def test_setup(self, mock_dependencies):
        logic = TransferLogic()
        logic.setup()

    def test_setup_table(self, mock_dependencies):
        logic = TransferLogic()
        logic.setup_table()
        mock_dependencies['table_model'].assert_called()
        assert logic.table.model() is not None

    def test_transfer_security_yes(self, mock_dependencies):
        logic = TransferLogic()
        with patch('app.controllers.finance.transfer.QMessageBox') as mock_qmsg:
            mock_qmsg_instance = MagicMock()
            mock_qmsg_instance.question = MagicMock(return_value=QMessageBox.StandardButton.Yes)
            mock_qmsg.return_value = mock_qmsg_instance
            with patch.object(logic, 'transfer_order') as mock_order:
                logic.transfer_security(Account.BANK)
                mock_order.assert_called_with(Account.BANK)

    def test_transfer_security_no(self, mock_dependencies):
        logic = TransferLogic()
        with patch('app.controllers.finance.transfer.QMessageBox') as mock_qmsg:
            mock_qmsg_instance = MagicMock()
            mock_qmsg_instance.question = MagicMock(return_value=QMessageBox.StandardButton.No)
            mock_qmsg.return_value = mock_qmsg_instance
            with patch.object(logic, 'reset') as mock_reset:
                logic.transfer_security(Account.BANK)
                mock_reset.assert_called()

    def test_transfer_order_success(self, mock_dependencies):
        logic = TransferLogic()
        logic.date.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-01')))
        logic.price.value = MagicMock(return_value=100)
        logic.note.text = MagicMock(return_value='Note')
        logic.manager = mock_dependencies['model']
        logic.transfer_order(Account.BANK)
        mock_dependencies['model'].create.assert_called()

    def test_transfer_order_validation_fail(self, mock_dependencies):
        logic = TransferLogic()
        entity = mock_dependencies['schema_factory'].TRANSFER.return_value
        entity.validate = MagicMock(return_value=False)
        logic.transfer_order(Account.BANK)
        mock_dependencies['error'].assert_called_with("الرجاء ملء جميع الحقول")

    def test_show_table(self, mock_dependencies):
        logic = TransferLogic()
        logic.operatore.currentText = MagicMock(return_value='op')
        logic.du.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-01')))
        logic.to.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-02')))
        logic.price.value = MagicMock(return_value=0)
        logic.manager = mock_dependencies['model']
        with patch.object(logic, 'set_totals') as mock_set_totals:
            logic.show_table()
            mock_dependencies['model'].get_filter.assert_called()
            mock_dependencies['model'].get_by_filter.assert_called()
            mock_dependencies['table_model'].refresh.assert_called()
            mock_set_totals.assert_called()

    def test_reset(self, mock_dependencies):
        logic = TransferLogic()
        logic.date.setDate = MagicMock()
        logic.price.setValue = MagicMock()
        logic.note.clear = MagicMock()
        logic.operatore.setCurrentIndex = MagicMock()
        logic.du.setDate = MagicMock()
        logic.to.setDate = MagicMock()
        logic.reset()
        # assertions

    def test_export(self, mock_dependencies):
        logic = TransferLogic()
        logic.model = mock_dependencies['table_model']
        logic.model.get_current_data = MagicMock(return_value=[MagicMock(price=10), MagicMock(price=20)])
        logic.manager = mock_dependencies['model']
        logic.export(ReportType.PRINT)
        mock_dependencies['model'].set_dynamic_metadata.assert_called_with(30, [MagicMock(), MagicMock()])
        mock_dependencies['model'].export_data.assert_called_with(report_type=ReportType.PRINT, parent=logic)

    def test_totals_to_bank(self, mock_dependencies):
        logic = TransferLogic()
        logic.manager = mock_dependencies['model']
        logic.totals_to_bank(price=100, operator='op', from_date='2026-01-01', to_date='2026-01-02')
        mock_dependencies['model'].get_filter.assert_called_with(from_date='2026-01-01', to_date='2026-01-02', price=100, operator='op', destination='البنك')
        mock_dependencies['model'].get_total.assert_called()

    def test_totals_to_caisse(self, mock_dependencies):
        logic = TransferLogic()
        logic.manager = mock_dependencies['model']
        logic.totals_to_caisse(price=100, operator='op', from_date='2026-01-01', to_date='2026-01-02')
        mock_dependencies['model'].get_filter.assert_called_with(from_date='2026-01-01', to_date='2026-01-02', price=100, operator='op', destination='الصندوق')
        mock_dependencies['model'].get_total.assert_called()

    def test_expense_income_totals(self, mock_dependencies):
        logic = TransferLogic()
        logic.income_manager = mock_dependencies['model']
        logic.expenses_manager = mock_dependencies['model']
        logic.expense_income_totals(price=100, operator='op', from_date='2026-01-01', to_date='2026-01-02', is_bank=True)
        mock_dependencies['model'].get_filter.assert_any_call(from_date='2026-01-01', to_date='2026-01-02', price=100, operator='op', is_bank=True)
        mock_dependencies['model'].get_total.assert_called()

    def test_totals_summary(self, mock_dependencies):
        logic = TransferLogic()
        with patch.object(logic, 'totals_to_bank', return_value=100) as mock_tb, \
             patch.object(logic, 'totals_to_caisse', return_value=30) as mock_tc, \
             patch.object(logic, 'expense_income_totals') as mock_eit:
            mock_eit.side_effect = [(200, 50), (300, 60)]  # for bank and caisse respectively
            summary = logic.totals_summary(price=100, operator='op', from_date='2026-01-01', to_date='2026-01-02')
            assert summary['total_to_bank'] == 100
            assert summary['total_to_caisse'] == 30
            assert summary['income_bank_total'] == 200
            assert summary['expense_bank_total'] == 50
            assert summary['income_caisse_total'] == 300
            assert summary['expense_caisse_total'] == 60

    def test_set_totals(self, mock_dependencies):
        logic = TransferLogic()
        with patch.object(logic, 'totals_summary', return_value={
            'total_to_bank': 100,
            'total_to_caisse': 30,
            'income_bank_total': 200,
            'expense_bank_total': 50,
            'income_caisse_total': 300,
            'expense_caisse_total': 60
        }) as mock_summary:
            logic.set_totals()
            # total_transfered = 100 - 30 = 70
            # total_in_bank = 200 - 50 + 70 = 220
            # total_in_caisse = 300 - 60 - 70 = 170
            assert logic.total_bank.text() == '220'
            assert logic.total_caisse.text() == '170'
