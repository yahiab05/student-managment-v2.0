from datetime import datetime
from unittest.mock import MagicMock

import pytest
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from app.controllers import mainWindow as main_window_module
from app.controllers.mainWindow import mainWindow
from app.controllers.controller_factory import ControllerSection


@pytest.fixture
def window(qapp, monkeypatch):
    """A mainWindow with the heavy internals (factory/section wiring,
    model lookups) short-circuited so we can test its own logic in
    isolation."""
    fake_factory = MagicMock()
    monkeypatch.setattr(
        main_window_module, "ControllerFactory", MagicMock(return_value=fake_factory)
    )
    monkeypatch.setattr(main_window_module, "get_model", MagicMock(return_value=MagicMock()))

    win = mainWindow()
    win._fake_factory = fake_factory
    return win


class TestMainWindowInit:
    def test_creates_a_controller_factory(self, window):
        main_window_module.ControllerFactory.assert_called_once()

    def test_wires_up_sections_with_stacked_widget_and_buttons(self, window):
        window._fake_factory.setup_sections.assert_called_once()
        args, kwargs = window._fake_factory.setup_sections.call_args
        stacked_widget, buttons = args
        assert stacked_widget is window.stackedWidget
        assert set(buttons.keys()) == {
            ControllerSection.ADMIN,
            ControllerSection.CLASSES,
            ControllerSection.TEACHERS,
            ControllerSection.PAYMENTS,
            ControllerSection.SETTINGS,
            ControllerSection.STUDENTS,
            ControllerSection.FINANCE,
        }

    def test_button_mapping_points_to_correct_widgets(self, window):
        _, buttons = window._fake_factory.setup_sections.call_args[0]
        assert buttons[ControllerSection.ADMIN] is window.user
        assert buttons[ControllerSection.CLASSES] is window.classes
        assert buttons[ControllerSection.TEACHERS] is window.teachers
        assert buttons[ControllerSection.PAYMENTS] is window.payment
        assert buttons[ControllerSection.SETTINGS] is window.settings
        assert buttons[ControllerSection.STUDENTS] is window.students
        assert buttons[ControllerSection.FINANCE] is window.money

    def test_fetches_access_manager(self, window):
        from app.models import ModelName
        main_window_module.get_model.assert_called_once_with(ModelName.ACCESS)


class TestCloseEvent:
    def _make_event(self):
        event = MagicMock()
        return event

    def test_backs_up_when_user_confirms(self, window, monkeypatch):
        monkeypatch.setattr(
            QMessageBox, "question", MagicMock(return_value=QMessageBox.StandardButton.Yes)
        )
        window.backup_mysql_db = MagicMock()
        event = self._make_event()

        window.closeEvent(event)

        window.backup_mysql_db.assert_called_once()
        event.accept.assert_called_once()

    def test_skips_backup_when_user_declines(self, window, monkeypatch):
        monkeypatch.setattr(
            QMessageBox, "question", MagicMock(return_value=QMessageBox.StandardButton.No)
        )
        window.backup_mysql_db = MagicMock()
        event = self._make_event()

        window.closeEvent(event)

        window.backup_mysql_db.assert_not_called()
        event.accept.assert_called_once()


class TestBackupMysqlDb:
    def _set_env(self, monkeypatch, **overrides):
        env = {
            "MYSQL_DATABASE": "school_db",
            "MYSQL_PWD": "s3cr3t",
            "MYSQL_HOST": "localhost",
            "MYSQL_PORT": "3306",
            "MYSQL_USER": "root",
        }
        env.update(overrides)
        for key, value in env.items():
            if value is None:
                monkeypatch.delenv(key, raising=False)
            else:
                monkeypatch.setenv(key, value)

    def test_returns_none_when_no_directory_chosen(self, window, monkeypatch):
        monkeypatch.setattr(
            QFileDialog, "getExistingDirectory", MagicMock(return_value="")
        )
        result = window.backup_mysql_db()
        assert result is None

    def test_raises_value_error_when_env_vars_missing(self, window, monkeypatch, tmp_path):
        monkeypatch.setattr(
            QFileDialog, "getExistingDirectory", MagicMock(return_value=str(tmp_path))
        )
        self._set_env(monkeypatch, MYSQL_PASSWORD=None, MYSQL_PWD=None)

        with pytest.raises(ValueError, match="Missing database environment variables"):
            window.backup_mysql_db()

    def test_successful_backup_runs_mysqldump_and_returns_path(
        self, window, monkeypatch, tmp_path
    ):
        monkeypatch.setattr(
            QFileDialog, "getExistingDirectory", MagicMock(return_value=str(tmp_path))
        )
        self._set_env(monkeypatch)

        fixed_now = datetime(2024, 1, 2, 3, 4, 5)
        fake_datetime = MagicMock()
        fake_datetime.now.return_value = fixed_now
        monkeypatch.setattr(main_window_module, "datetime", fake_datetime)

        fake_run = MagicMock(return_value=MagicMock(returncode=0))
        monkeypatch.setattr(main_window_module, "run", fake_run)

        result = window.backup_mysql_db()

        expected_file = tmp_path / "school_db_2024-01-02_03-04-05.sql"
        assert result == str(expected_file)
        assert expected_file.exists()

        fake_run.assert_called_once()
        cmd = fake_run.call_args.args[0]
        assert cmd == [
            "mysqldump",
            "-h", "localhost",
            "-P", "3306",
            "-u", "root",
            "--routines",
            "--triggers",
            "--single-transaction",
            "--databases", "school_db",
        ]
        assert fake_run.call_args.kwargs["env"]["MYSQL_PWD"] == "s3cr3t"

    def test_failed_backup_raises_runtime_error_and_cleans_up_partial_file(
        self, window, monkeypatch, tmp_path
    ):
        monkeypatch.setattr(
            QFileDialog, "getExistingDirectory", MagicMock(return_value=str(tmp_path))
        )
        self._set_env(monkeypatch)

        fixed_now = datetime(2024, 1, 2, 3, 4, 5)
        fake_datetime = MagicMock()
        fake_datetime.now.return_value = fixed_now
        monkeypatch.setattr(main_window_module, "datetime", fake_datetime)

        fake_run = MagicMock(
            return_value=MagicMock(returncode=1, stderr=b"access denied")
        )
        monkeypatch.setattr(main_window_module, "run", fake_run)

        with pytest.raises(RuntimeError, match="mysqldump failed"):
            window.backup_mysql_db()

        expected_file = tmp_path / "school_db_2024-01-02_03-04-05.sql"
        assert not expected_file.exists()


class TestAccessControl:
    def test_sets_enabled_state_for_every_section_button(self, window):
        window.access_manager = MagicMock()
        window.access_manager.get_access.side_effect = lambda key: key == "teachers"

        for name in ("students", "classes", "teachers", "payment", "money", "settings", "user"):
            setattr(window, name, MagicMock())

        window.access_control()

        window.students.setEnabled.assert_called_once_with(False)
        window.classes.setEnabled.assert_called_once_with(False)
        window.teachers.setEnabled.assert_called_once_with(True)
        window.payment.setEnabled.assert_called_once_with(False)
        window.money.setEnabled.assert_called_once_with(False)
        window.settings.setEnabled.assert_called_once_with(False)
        window.user.setEnabled.assert_called_once_with(False)
