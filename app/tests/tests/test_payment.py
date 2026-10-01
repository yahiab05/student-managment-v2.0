# test_payments.py
import pytest
from unittest.mock import DEFAULT, MagicMock, patch
from PyQt6.QtCore import QDate

from app.controllers.payment.payments import ViewPayment
from app.controllers.payment.not_payed_view import ViewNotPayedLogic
from app.controllers.payment import PaymentPart
from app.utils import ReportType


@pytest.fixture(autouse=True)
def mock_payment_deps():
    with patch.multiple(
        'app.controllers.payment.payments',
        load_gui=DEFAULT,
        get_model=DEFAULT,
        get_student_list=DEFAULT,
        get_combo_manager=DEFAULT,
        create_table_model=DEFAULT,
        error=DEFAULT,
    ) as payment_mocks, patch.multiple(
        'app.controllers.payment.not_payed_view',
        load_gui=DEFAULT,
        get_model=DEFAULT,
        get_combo_manager=DEFAULT,
        error=DEFAULT,
    ) as not_payed_mocks, patch.multiple(
        'app.controllers.payment.__init__',
        load_gui=DEFAULT,
    ) as payment_part_mocks:
        mock_load_pay = payment_mocks['load_gui']
        mock_get_model = payment_mocks['get_model']
        mock_student_list = payment_mocks['get_student_list']
        mock_combo = payment_mocks['get_combo_manager']
        mock_create_table = payment_mocks['create_table_model']
        mock_error = payment_mocks['error']
        mock_load_not = not_payed_mocks['load_gui']
        mock_get_model_not = not_payed_mocks['get_model']
        mock_combo_not = not_payed_mocks['get_combo_manager']
        mock_error_not = not_payed_mocks['error']
        mock_load_part = payment_part_mocks['load_gui']
        
        mock_model = MagicMock()
        mock_model.get_total = MagicMock(return_value=100)
        mock_model.get_by_filter = MagicMock(return_value=[])
        mock_model.get_filter = MagicMock(return_value={})
        mock_model.refresh = MagicMock()
        mock_model.rowCount = MagicMock(return_value=5)
        mock_model.get_by_id = MagicMock(return_value=MagicMock(price=150))
        mock_model.update_price = MagicMock()
        mock_model.rollback = MagicMock()
        mock_model.set_dynamic_metadata = MagicMock()
        mock_model.export_data = MagicMock()
        mock_model.get_current_data = MagicMock(return_value=[])
        mock_model.get_access = MagicMock(return_value=True)
        mock_model.get_by_filter.return_value = []

        def get_model_side_effect(name):
            if name in ['INCOME', 'PAYMENTS', 'ENROLLMENT', 'ACCESS']:
                return mock_model
            return MagicMock()
        mock_get_model.side_effect = get_model_side_effect
        mock_get_model_not.side_effect = get_model_side_effect

        mock_combo_mgr = MagicMock()
        mock_combo_mgr.update_combo = MagicMock()
        mock_combo_mgr.update_combo.return_value = None
        mock_combo.return_value = mock_combo_mgr
        mock_combo_not.return_value = mock_combo_mgr

        mock_student_list.return_value = [MagicMock(name='Student A'), MagicMock(name='Student B')]

        mock_table_model = MagicMock()
        mock_table_model.ID_COLUMN = 0
        mock_table_model.rowCount = MagicMock(return_value=5)
        mock_table_model.data = MagicMock(return_value=42)
        mock_table_model.get_current_data = MagicMock(return_value=[])
        mock_table_model.refresh = MagicMock()
        mock_create_table.return_value = mock_table_model

        yield {
            'load_pay': mock_load_pay,
            'load_not': mock_load_not,
            'load_part': mock_load_part,
            'get_model': mock_get_model,
            'model': mock_model,
            'combo': mock_combo_mgr,
            'student_list': mock_student_list,
            'table_model': mock_table_model,
            'error': mock_error,
            'error_not': mock_error_not,
        }


# --- ViewPayment tests ---
class TestViewPayment:
    def test_init(self, mock_payment_deps):
        with patch('app.controllers.payment.payments.ViewPaymentUI'):
            view = ViewPayment()
            mock_payment_deps['load_pay'].assert_called()
            assert view.manager is not None
            assert view.model is not None
            mock_payment_deps['model'].get_total.assert_called()
            assert view.total.text() == '100'

    def test_setup(self, mock_payment_deps):
        view = ViewPayment()
        view.setup()

    def test_setup_table(self, mock_payment_deps):
        view = ViewPayment()
        view.setup_table()
        mock_payment_deps['table_model'].assert_called()
        assert view.reg_tbl.model() is not None
        assert view.total.text() == '100'
        assert view.nb.text() == '5'

    def test_search(self, mock_payment_deps):
        view = ViewPayment()
        view.search_ent.text = MagicMock(return_value='Student')
        view.du.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-01')))
        view.to.date = MagicMock(return_value=MagicMock(toPyDate=MagicMock(return_value='2026-01-02')))
        view.classroom.currentText = MagicMock(return_value='Class A')
        view.num_inscrit.text = MagicMock(return_value='123')
        view.way.currentText = MagicMock(return_value='Cash')
        view.manager = mock_payment_deps['model']
        view.search()
        mock_payment_deps['model'].get_filter.assert_called_with(
            classroom='Class A', name='Student', way='Cash',
            payment_from_date='2026-01-01', payment_to_date='2026-01-02',
            num_inscrit='123'
        )
        mock_payment_deps['table_model'].refresh.assert_called()
        assert view.total.text() == '100'
        assert view.nb.text() == '5'

    def test_select_student(self, mock_payment_deps):
        view = ViewPayment()
        view.student_list = MagicMock()
        view.student_list.currentItem = MagicMock(return_value=MagicMock(text=MagicMock(return_value='Student A')))
        view.search_ent.setText = MagicMock()
        view.select_student()
        view.search_ent.setText.assert_called_with('Student A')

    def test_show_students_list(self, mock_payment_deps):
        view = ViewPayment()
        view.student_list = MagicMock()
        view.student_list.clear = MagicMock()
        view.student_list.addItem = MagicMock()
        view.show_students_list('')
        mock_payment_deps['student_list'].assert_called_with('')
        assert view.student_list.addItem.call_count == 2

    def test_reset(self, mock_payment_deps):
        view = ViewPayment()
        view.search_ent.setText = MagicMock()
        view.du.setDate = MagicMock()
        view.to.setDate = MagicMock()
        view.classroom.setCurrentIndex = MagicMock()
        view.way.setCurrentIndex = MagicMock()
        view.num_inscrit.setText = MagicMock()
        with patch.object(view, 'show_students_list') as mock_show:
            view.reset()
            view.search_ent.setText.assert_called_with('')
            view.num_inscrit.setText.assert_called_with('')
            mock_show.assert_called()

    def test_select_row_success(self, mock_payment_deps):
        view = ViewPayment()
        view.has_access = MagicMock(return_value=True)
        view.model = mock_payment_deps['table_model']
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = [MagicMock(row=MagicMock(return_value=0))]
        view.reg_tbl.selectionModel = MagicMock(return_value=mock_selection)
        view.stackedWidget.setCurrentIndex = MagicMock()
        view.search_frame.setEnabled = MagicMock()
        with patch.object(view, 'set_old_price') as mock_set_old:
            view.select_row()
            assert view.identifier == 42
            view.stackedWidget.setCurrentIndex.assert_called_with(1)
            view.search_frame.setEnabled.assert_called_with(False)
            mock_set_old.assert_called_with(42)

    def test_select_row_no_selection(self, mock_payment_deps):
        view = ViewPayment()
        view.has_access = MagicMock(return_value=True)
        mock_selection = MagicMock()
        mock_selection.selectedRows.return_value = []
        view.reg_tbl.selectionModel = MagicMock(return_value=mock_selection)
        view.select_row()
        mock_payment_deps['error'].assert_called_with("يرجى تحديد وصل:")

    def test_select_row_no_access(self, mock_payment_deps):
        view = ViewPayment()
        view.has_access = MagicMock(return_value=False)
        view.select_row()
        mock_payment_deps['error'].assert_called_with("ليس لديك صلاحية")

    def test_set_old_price(self, mock_payment_deps):
        view = ViewPayment()
        view.previous_price = MagicMock()
        view.manager = mock_payment_deps['model']
        view.set_old_price(1)
        mock_payment_deps['model'].get_by_id.assert_called_with(1)
        view.previous_price.setText.assert_called_with('150')

    def test_has_access(self, mock_payment_deps):
        view = ViewPayment()
        result = view.has_access()
        assert result is True
        mock_payment_deps['model'].get_access.assert_called_with("payment_edit")

    def test_edit_price_success(self, mock_payment_deps):
        view = ViewPayment()
        view.identifier = 1
        view.new_price = MagicMock()
        view.new_price.value = MagicMock(return_value=200)
        view.manager = mock_payment_deps['model']
        with patch.object(view, 'cancel') as mock_cancel, patch.object(view, 'setup_table') as mock_setup:
            view.edit_price()
            mock_payment_deps['model'].update_price.assert_called_with(1, 200)
            mock_cancel.assert_called()
            mock_setup.assert_called()

    def test_edit_price_zero(self, mock_payment_deps):
        view = ViewPayment()
        view.new_price = MagicMock()
        view.new_price.value = MagicMock(return_value=0)
        view.edit_price()
        mock_payment_deps['error'].assert_called_with("السعر يجب ان يكون اكبر من صفر")

    def test_cancel(self, mock_payment_deps):
        view = ViewPayment()
        view.stackedWidget.setCurrentIndex = MagicMock()
        view.new_price.setValue = MagicMock()
        view.previous_price.setText = MagicMock()
        view.search_frame.setEnabled = MagicMock()
        view.cancel()
        view.stackedWidget.setCurrentIndex.assert_called_with(0)
        view.new_price.setValue.assert_called_with(0)
        view.previous_price.setText.assert_called_with('')
        view.search_frame.setEnabled.assert_called_with(True)

    def test_populate_combos(self, mock_payment_deps):
        view = ViewPayment()
        view.populate_combos()
        mock_payment_deps['combo'].update_combo.assert_any_call(view.way, 'WAY_PAYMENT')
        mock_payment_deps['combo'].update_combo.assert_any_call(view.classroom, 'CLASS')

    def test_export(self, mock_payment_deps):
        view = ViewPayment()
        view.model = mock_payment_deps['table_model']
        view.model.get_current_data = MagicMock(return_value=[])
        view.manager = mock_payment_deps['model']
        view.export(ReportType.PRINT)
        mock_payment_deps['model'].set_dynamic_metadata.assert_called_with(data_to_export=[], total_price=100)
        mock_payment_deps['model'].export_data.assert_called_with(report_type=ReportType.PRINT, parent=view)


# --- ViewNotPayedLogic tests ---
class TestViewNotPayedLogic:
    def test_init(self, mock_payment_deps):
        with patch('app.controllers.payment.not_payed_view.ViewNotPayedUI'):
            view = ViewNotPayedLogic()
            mock_payment_deps['load_not'].assert_called()
            assert view.manager is not None
            assert view.month.value() == 1
            assert view.year.value() == QDate.currentDate().year()

    def test_setup(self, mock_payment_deps):
        view = ViewNotPayedLogic()
        view.setup()

    def test_search_with_class(self, mock_payment_deps):
        view = ViewNotPayedLogic()
        view.classroom.currentText = MagicMock(return_value='Class A')
        view.month.value = MagicMock(return_value=1)
        view.year.value = MagicMock(return_value=2026)
        view.manager = mock_payment_deps['model']
        view.enrollment_manager = mock_payment_deps['model']
        view.tbl = MagicMock()
        view.tbl.clear = MagicMock()
        view.tbl.addItem = MagicMock()
        # mock data
        mock_payment_deps['model'].get_by_filter.return_value = [MagicMock(id=1)]
        mock_payment_deps['model'].get_filters.return_value = {}
        mock_payment_deps['model'].get_by_filter.return_value = [MagicMock(students=MagicMock(name='Student X'))]
        view.search()
        mock_payment_deps['model'].get_filter.assert_called_with(classroom='Class A', year=2026, month=1)
        view.tbl.addItem.assert_called_with('Student X')

    def test_search_no_class(self, mock_payment_deps):
        view = ViewNotPayedLogic()
        view.classroom.currentText = MagicMock(return_value='')
        view.search()
        mock_payment_deps['error_not'].assert_called_with("يرجى تحديد الصف")

    def test_search_insurance(self, mock_payment_deps):
        view = ViewNotPayedLogic()
        view.classroom.currentText = MagicMock(return_value='تأمين')
        view.manager = mock_payment_deps['model']
        view.enrollment_manager = mock_payment_deps['model']
        view.tbl = MagicMock()
        view.tbl.clear = MagicMock()
        view.tbl.addItem = MagicMock()
        mock_payment_deps['model'].get_by_filter.return_value = [MagicMock(id=1)]
        mock_payment_deps['model'].get_filters.return_value = {}
        mock_payment_deps['model'].get_by_filter.return_value = [MagicMock(name='Student Y')]
        view.search()
        mock_payment_deps['model'].get_filter.assert_called_with(classroom='تأمين', year=2026)
        view.tbl.addItem.assert_called_with('Student Y')

    def test_reset(self, mock_payment_deps):
        view = ViewNotPayedLogic()
        view.classroom.setCurrentIndex = MagicMock()
        view.month.setValue = MagicMock()
        view.year.setValue = MagicMock()
        view.reset()
        view.classroom.setCurrentIndex.assert_called_with(-1)
        view.month.setValue.assert_called_with(1)
        view.year.setValue.assert_called_with(QDate.currentDate().year())

    def test_populate_classes(self, mock_payment_deps):
        view = ViewNotPayedLogic()
        view.populate_classes()
        mock_payment_deps['combo'].update_combo.assert_called_with(view.classroom, 'CLASSES')


# --- PaymentPart tests ---
class TestPaymentPart:
    def test_init(self, mock_payment_deps):
        with patch('app.controllers.payment.__init__.PaymentPartUI'):
            part = PaymentPart()
            mock_payment_deps['load_part'].assert_called()
            assert part.stackedWidget.count() == 2

    def test_setup(self, mock_payment_deps):
        part = PaymentPart()
        part.setup()

    def test_go_to_view_payment(self, mock_payment_deps):
        part = PaymentPart()
        part.vp = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.view_payment = MagicMock()
        part.go_to_view_payment()
        part.stackedWidget.setCurrentIndex.assert_called_with(1)
        part.vp.populate_combos.assert_called()
        part.vp.setup_table.assert_called()
        part.vp.show_students_list.assert_called()
        part.buttons.assert_called_with(part.view_payment)

    def test_go_to_view_not_payed(self, mock_payment_deps):
        part = PaymentPart()
        part.vnp = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.view_not_payed = MagicMock()
        part.go_to_view_not_payed()
        part.stackedWidget.setCurrentIndex.assert_called_with(2)
        part.vnp.populate_classes.assert_called()
        part.buttons.assert_called_with(part.view_not_payed)

    def test_buttons(self, mock_payment_deps):
        part = PaymentPart()
        part.view_payment = MagicMock()
        part.view_not_payed = MagicMock()
        button = MagicMock()
        part.buttons(button)
        part.view_payment.setStyleSheet.assert_called_with("color: white")
        part.view_not_payed.setStyleSheet.assert_called_with("color: white")
        button.setStyleSheet.assert_called_with("color: green")