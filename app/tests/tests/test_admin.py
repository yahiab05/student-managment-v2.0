# test_admin.py
import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QTableWidgetItem

from app.controllers.others.admin import RoleLogic, UserLogic, UserPart
from app.utils import WorkingMode, ComboName


@pytest.fixture(autouse=True)
def mock_admin_deps():
    """Mock dependencies for admin tests."""
    with patch('app.controllers.others.admin.load_gui') as mock_load, \
         patch('app.controllers.others.admin.get_model') as mock_get_model, \
         patch('app.controllers.others.admin.get_combo_manager') as mock_combo, \
         patch('app.controllers.others.admin.error') as mock_error, \
         patch('app.controllers.others.admin.SchemaFactory') as mock_schema:
        
        mock_model = MagicMock()
        mock_model.create = MagicMock()
        mock_model.update_by_filter = MagicMock()
        mock_model.delete_by_filter = MagicMock()
        mock_model.get_filter = MagicMock(return_value={})
        mock_model.get_by_filter = MagicMock(return_value=[MagicMock()])
        mock_model.update = MagicMock()
        mock_model.delete = MagicMock()
        mock_model.get_all = MagicMock(return_value=[MagicMock(id=1, username='u1', password='p1', role_name='r1')])
        mock_model.update_cache_from_db = MagicMock()
        mock_model.get_access = MagicMock(return_value=True)

        def get_model_side_effect(name):
            if name in ['ROLES', 'USERS', 'ACCESS']:
                return mock_model
            return MagicMock()
        mock_get_model.side_effect = get_model_side_effect

        mock_combo_mgr = MagicMock()
        mock_combo_mgr.update_combo = MagicMock()
        mock_combo_mgr.update_cache_from_db = MagicMock()
        mock_combo.return_value = mock_combo_mgr

        mock_entity = MagicMock()
        mock_entity.validate = MagicMock(return_value=True)
        mock_schema.ROLE.return_value = mock_entity
        mock_schema.USER.return_value = mock_entity

        yield {
            'load': mock_load,
            'get_model': mock_get_model,
            'combo': mock_combo_mgr,
            'error': mock_error,
            'schema': mock_schema,
            'model': mock_model,
        }


# --- RoleLogic tests ---
class TestRoleLogic:
    def test_init(self, mock_admin_deps):
        with patch('app.controllers.others.admin.RoleUI'):
            logic = RoleLogic()
            mock_admin_deps['load'].assert_called()
            assert logic.manager is not None
            mock_admin_deps['combo'].update_combo.assert_called_with(logic.name_search, ComboName.ROLE)

    def test_setup(self, mock_admin_deps):
        logic = RoleLogic()
        logic.setup()
        # signals connected; we can't easily test but we check attributes exist
        assert hasattr(logic.search_btn, 'clicked')

    def test_control_add_success(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name.text = MagicMock(return_value='admin')
        logic.students.isChecked = MagicMock(return_value=True)
        logic.teachers.isChecked = MagicMock(return_value=False)
        # mock other checkboxes
        with patch.object(logic, 'combo_manager') as mock_combo:
            logic.control(WorkingMode.ADD)
            mock_admin_deps['model'].create.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.ROLE)

    def test_control_update_success(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name.text = MagicMock(return_value='admin')
        logic.name_selected = 'old_role'
        logic.manager = mock_admin_deps['model']
        with patch.object(logic, 'combo_manager') as mock_combo:
            logic.control(WorkingMode.UPDATE)
            mock_admin_deps['model'].update_by_filter.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.ROLE)

    def test_control_update_no_selected(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name_selected = ''
        logic.control(WorkingMode.UPDATE)
        mock_admin_deps['error'].assert_called_with("يرجى تحديد دور")

    def test_control_validation_fail(self, mock_admin_deps):
        logic = RoleLogic()
        entity = mock_admin_deps['schema'].ROLE.return_value
        entity.validate = MagicMock(return_value=False)
        logic.control(WorkingMode.ADD)
        mock_admin_deps['error'].assert_called_with("الرجاء التحقق من صحة البيانات")

    def test_select_role(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name_search.currentText = MagicMock(return_value='RoleX')
        mock_model = mock_admin_deps['model']
        role_data = MagicMock()
        role_data.students = True
        role_data.teachers = False
        role_data.classes = True
        role_data.absent = False
        role_data.money = True
        role_data.settings = False
        role_data.user = True
        role_data.payment_editting = False
        mock_model.get_by_filter.return_value = [role_data]
        logic.manager = mock_model
        logic.select_role()
        assert logic.name_selected == 'RoleX'
        assert logic.students.setChecked.called
        # etc.

    def test_select_role_no_data(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name_search.currentText = MagicMock(return_value='RoleX')
        mock_model = mock_admin_deps['model']
        mock_model.get_by_filter.return_value = []
        logic.manager = mock_model
        logic.select_role()
        # no checkboxes set, nothing should happen

    def test_delete_role_success(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name_selected = 'RoleX'
        logic.manager = mock_admin_deps['model']
        with patch.object(logic, 'combo_manager') as mock_combo:
            logic.delete_role()
            mock_admin_deps['model'].delete_by_filter.assert_called()
            mock_combo.update_cache_from_db.assert_called_with(ComboName.ROLE)

    def test_delete_role_no_selected(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name_selected = ''
        logic.delete_role()
        mock_admin_deps['error'].assert_called_with("يرجى تحديد دور")

    def test_populate_combo(self, mock_admin_deps):
        logic = RoleLogic()
        logic.populate_combo()
        mock_admin_deps['combo'].update_combo.assert_called_with(logic.name_search, ComboName.ROLE)

    def test_reset(self, mock_admin_deps):
        logic = RoleLogic()
        logic.name.setText = MagicMock()
        logic.name_search.setCurrentIndex = MagicMock()
        logic.students.setChecked = MagicMock()
        logic.reset()
        assert logic.name_selected == ''
        logic.name.setText.assert_called_with('')
        logic.name_search.setCurrentIndex.assert_called_with(-1)

    def test_select_deselect_all(self, mock_admin_deps):
        logic = RoleLogic()
        logic.students.setChecked = MagicMock()
        logic.teachers.setChecked = MagicMock()
        logic.classes.setChecked = MagicMock()
        logic.payment.setChecked = MagicMock()
        logic.absents.setChecked = MagicMock()
        logic.money.setChecked = MagicMock()
        logic.settings.setChecked = MagicMock()
        logic.user.setChecked = MagicMock()
        logic.payment_edit.setChecked = MagicMock()
        logic.select_deselect_all()
        for cb in [logic.students, logic.teachers, logic.classes, logic.payment, 
                   logic.absents, logic.money, logic.settings, logic.user, logic.payment_edit]:
            cb.setChecked.assert_called_with(True)


# --- UserLogic tests ---
class TestUserLogic:
    def test_init(self, mock_admin_deps):
        with patch('app.controllers.others.admin.UserUI'):
            logic = UserLogic()
            mock_admin_deps['load'].assert_called()
            assert logic.manager is not None
            mock_admin_deps['model'].get_all.assert_called()
            mock_admin_deps['combo'].update_combo.assert_called_with(logic.role, ComboName.ROLE)

    def test_setup(self, mock_admin_deps):
        logic = UserLogic()
        logic.setup()

    def test_reset(self, mock_admin_deps):
        logic = UserLogic()
        logic.user.setText = MagicMock()
        logic.passwd.setText = MagicMock()
        logic.role.setCurrentIndex = MagicMock()
        logic.reset()
        logic.user.setText.assert_called_with('')
        logic.passwd.setText.assert_called_with('')
        logic.role.setCurrentIndex.assert_called_with(-1)

    def test_control_add_success(self, mock_admin_deps):
        logic = UserLogic()
        logic.user.text = MagicMock(return_value='user')
        logic.passwd.text = MagicMock(return_value='pass')
        logic.role.currentText = MagicMock(return_value='role')
        with patch.object(logic, 'show_users') as mock_show, patch.object(logic, 'reset') as mock_reset:
            logic.control(WorkingMode.ADD)
            mock_admin_deps['model'].create.assert_called()
            mock_show.assert_called()
            mock_reset.assert_called()

    def test_control_update_success(self, mock_admin_deps):
        logic = UserLogic()
        logic.identifier = 1
        logic.user.text = MagicMock(return_value='user')
        logic.passwd.text = MagicMock(return_value='pass')
        logic.role.currentText = MagicMock(return_value='role')
        with patch.object(logic, 'show_users') as mock_show, patch.object(logic, 'reset') as mock_reset:
            logic.control(WorkingMode.UPDATE)
            mock_admin_deps['model'].update.assert_called_with(1, mock_admin_deps['schema'].USER.return_value)
            mock_show.assert_called()
            mock_reset.assert_called()
            assert logic.identifier is None

    def test_control_update_no_identifier(self, mock_admin_deps):
        logic = UserLogic()
        logic.identifier = None
        logic.control(WorkingMode.UPDATE)
        mock_admin_deps['error'].assert_called_with("يرجى تحديد مستخدم")

    def test_control_validation_fail(self, mock_admin_deps):
        logic = UserLogic()
        entity = mock_admin_deps['schema'].USER.return_value
        entity.validate = MagicMock(return_value=False)
        logic.control(WorkingMode.ADD)
        mock_admin_deps['error'].assert_called_with("الرجاء التحقق من صحة البيانات")

    def test_select_user(self, mock_admin_deps):
        logic = UserLogic()
        logic.tbl = MagicMock()
        logic.tbl.currentRow = MagicMock(return_value=0)
        logic.tbl.item = MagicMock(side_effect=[
            MagicMock(text=MagicMock(return_value='1')),
            MagicMock(text=MagicMock(return_value='user')),
            MagicMock(text=MagicMock(return_value='pass')),
            MagicMock(text=MagicMock(return_value='role'))
        ])
        logic.user.setText = MagicMock()
        logic.passwd.setText = MagicMock()
        logic.role.setCurrentText = MagicMock()
        logic.select_user()
        assert logic.identifier == '1'
        logic.user.setText.assert_called_with('user')
        logic.passwd.setText.assert_called_with('pass')
        logic.role.setCurrentText.assert_called_with('role')

    def test_delete_success(self, mock_admin_deps):
        logic = UserLogic()
        logic.identifier = 1
        with patch.object(logic, 'show_users') as mock_show, patch.object(logic, 'reset') as mock_reset:
            logic.delete()
            mock_admin_deps['model'].delete.assert_called_with(1)
            mock_show.assert_called()
            mock_reset.assert_called()
            assert logic.identifier is None

    def test_delete_no_identifier(self, mock_admin_deps):
        logic = UserLogic()
        logic.identifier = None
        logic.delete()
        mock_admin_deps['error'].assert_called_with("يرجى تحديد مستخدم")

    def test_show_users(self, mock_admin_deps):
        logic = UserLogic()
        logic.tbl = MagicMock()
        logic.tbl.setItem = MagicMock()
        users = [
            MagicMock(id=1, username='u1', password='p1', role_name='r1'),
            MagicMock(id=2, username='u2', password='p2', role_name='r2')
        ]
        mock_admin_deps['model'].get_all.return_value = users
        logic.show_users()
        assert logic.tbl.setItem.call_count == 8  # 2 users * 4 columns

    def test_populate_combo(self, mock_admin_deps):
        logic = UserLogic()
        logic.populate_combo()
        mock_admin_deps['combo'].update_combo.assert_called_with(logic.role, ComboName.ROLE)


# --- UserPart tests ---
class TestUserPart:
    def test_init(self, mock_admin_deps):
        with patch('app.controllers.others.__init__.UserPartUI'):
            from app.controllers.others import UserPart
            part = UserPart()
            mock_admin_deps['load'].assert_called()
            assert part.stackedWidget.count() == 2

    def test_setup(self, mock_admin_deps):
        from app.controllers.others import UserPart
        part = UserPart()
        part.setup()

    def test_go_to_users(self, mock_admin_deps):
        from app.controllers.others import UserPart
        part = UserPart()
        part.u = MagicMock()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.user = MagicMock()
        part.go_to_users()
        part.stackedWidget.setCurrentIndex.assert_called_with(0)
        part.u.populate_combo.assert_called()
        part.buttons.assert_called_with(part.user)

    def test_go_to_roles(self, mock_admin_deps):
        from app.controllers.others import UserPart
        part = UserPart()
        part.stackedWidget.setCurrentIndex = MagicMock()
        part.add_role = MagicMock()
        part.go_to_roles()
        part.stackedWidget.setCurrentIndex.assert_called_with(1)
        part.buttons.assert_called_with(part.add_role)

    def test_buttons(self, mock_admin_deps):
        from app.controllers.others import UserPart
        part = UserPart()
        part.user = MagicMock()
        part.add_role = MagicMock()
        button = MagicMock()
        part.buttons(button)
        part.user.setStyleSheet.assert_called_with("color: white")
        part.add_role.setStyleSheet.assert_called_with("color: white")
        button.setStyleSheet.assert_called_with("color: green")