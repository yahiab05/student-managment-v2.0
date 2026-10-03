from unittest.mock import MagicMock, patch

from app.controllers.finance import BalanceLogic, OutMoneyLogic, EnteryLogic, TransferLogic, MoneyPart
from app.utils.utils import ReportType, WorkingMode, Account
from PyQt6.QtWidgets import QMessageBox


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
