from unittest.mock import MagicMock

import pytest

import app.controllers as controllers_module


class TestMain:
    def test_main_creates_app_shows_login_window_and_runs_event_loop(self, monkeypatch):
        fake_app_instance = MagicMock()
        fake_qapplication_cls = MagicMock(return_value=fake_app_instance)
        fake_login_instance = MagicMock()
        fake_login_cls = MagicMock(return_value=fake_login_instance)

        monkeypatch.setattr(controllers_module, "QApplication", fake_qapplication_cls)
        monkeypatch.setattr(controllers_module, "Login", fake_login_cls)

        controllers_module.main()

        fake_qapplication_cls.assert_called_once_with([])
        fake_login_cls.assert_called_once_with()
        fake_login_instance.show.assert_called_once()
        fake_app_instance.exec.assert_called_once()

    def test_main_shows_window_before_starting_event_loop(self, monkeypatch):
        call_order = []

        fake_app_instance = MagicMock()
        fake_app_instance.exec.side_effect = lambda: call_order.append("exec")
        fake_login_instance = MagicMock()
        fake_login_instance.show.side_effect = lambda: call_order.append("show")

        monkeypatch.setattr(
            controllers_module, "QApplication", MagicMock(return_value=fake_app_instance)
        )
        monkeypatch.setattr(
            controllers_module, "Login", MagicMock(return_value=fake_login_instance)
        )

        controllers_module.main()

        assert call_order == ["show", "exec"]
