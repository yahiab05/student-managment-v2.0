from unittest.mock import MagicMock, patch

from app.controllers.classes import ClassesLogic, ClasseleveLogic, ClassPart
from app.utils import ReportType, WorkingMode
from PyQt6.QtWidgets import QMessageBox


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


