from unittest.mock import MagicMock, call

import pytest

from app.controllers import login as login_module
from app.controllers.login import Login
from app.utils import UiPath


@pytest.fixture
def patched_dependencies(monkeypatch):
    """Patch every external dependency used by Login.__init__."""
    mocks = {
        "create_db": MagicMock(),
        "load_gui": MagicMock(),
        "get_model": MagicMock(side_effect=lambda name: MagicMock(name=f"model-{name}")),
        "set_username": MagicMock(),
        "mainWindow": MagicMock(),
    }
    for attr, mock in mocks.items():
        monkeypatch.setattr(login_module, attr, mock)
    return mocks


@pytest.fixture
def login_widget(qapp, patched_dependencies):
    return Login()


class TestLoginInit:
    def test_creates_db_on_init(self, qapp, patched_dependencies):
        Login()
        patched_dependencies["create_db"].assert_called_once()

    def test_loads_correct_ui_file(self, qapp, patched_dependencies):
        widget = Login()
        patched_dependencies["load_gui"].assert_called_once_with(
            UiPath.LOGIN, "login.ui", widget
        )

    def test_fetches_login_and_access_models(self, qapp, patched_dependencies):
        Login()
        from app.models import ModelName
        patched_dependencies["get_model"].assert_any_call(ModelName.LOGIN)
        patched_dependencies["get_model"].assert_any_call(ModelName.ACCESS)
        assert patched_dependencies["get_model"].call_count == 2


class TestLoginSetup:
    def test_setup_connects_submit_button_to_check_login(self, login_widget):
        login_widget.submit = MagicMock()
        login_widget.setup()
        login_widget.submit.clicked.connect.assert_called_once_with(
            login_widget.check_login
        )


class TestCheckLogin:
    def _configure_fields(self, widget, username="alice", password="secret"):
        widget.username = MagicMock()
        widget.username.text.return_value = username
        widget.password = MagicMock()
        widget.password.text.return_value = password

    def test_successful_login_triggers_open_app(self, login_widget):
        self._configure_fields(login_widget)
        login_widget.manager.check_login.return_value = True
        login_widget.open_app = MagicMock()

        login_widget.check_login()

        login_widget.manager.check_login.assert_called_once_with("alice", "secret")
        login_widget.open_app.assert_called_once_with("alice")

    def test_failed_login_does_not_trigger_open_app(self, login_widget):
        self._configure_fields(login_widget)
        login_widget.manager.check_login.return_value = False
        login_widget.open_app = MagicMock()

        login_widget.check_login()

        login_widget.open_app.assert_not_called()


class TestOpenApp:
    def test_open_app_sets_username_grants_access_and_shows_main_window(
        self, login_widget, patched_dependencies
    ):
        login_widget.set_access = MagicMock()
        login_widget.close = MagicMock()

        login_widget.open_app("bob")

        patched_dependencies["set_username"].assert_called_once_with("bob")
        login_widget.set_access.assert_called_once_with("bob")
        patched_dependencies["mainWindow"].assert_called_once()
        main_window_instance = patched_dependencies["mainWindow"].return_value
        main_window_instance.show.assert_called_once()
        login_widget.close.assert_called_once()


class TestSetAccess:
    def test_set_access_configures_access_manager(self, login_widget):
        login_widget.set_access("carol")

        login_widget.access_manager.set_user.assert_called_once_with("carol")
        login_widget.access_manager.set_access.assert_called_once()
