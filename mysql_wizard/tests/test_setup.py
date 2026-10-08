from unittest.mock import MagicMock, call

import pytest
from PyQt6.QtWidgets import QMessageBox

from mysql_wizard.core.setup import WizardPage


@pytest.fixture
def page(qapp):
    return WizardPage()


@pytest.fixture
def connection():
    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value = MagicMock()
    return connection


def test_setup_loads_ui_and_connects_migrate_signal(page):
    assert page.database_name.text() == ""
    assert page.pushButton.text() == "Migrate"
    assert page.pushButton.receivers(page.pushButton.clicked) == 1


def test_connect_to_database_closes_previous_connection_and_passes_credentials(
    page, connection
):
    previous = MagicMock()
    page.connection = previous
    page.connection_factory = MagicMock(return_value=connection)
    page.host = "db"
    page.port = 3307
    page.root_user = "root-user"
    page.root_password = "secret"

    result = page.connect_to_database("legacy_db")

    previous.close.assert_called_once_with()
    page.connection_factory.assert_called_once_with(
        host="db",
        port=3307,
        user="root-user",
        password="secret",
        autocommit=True,
        database="legacy_db",
    )
    connection.ping.assert_called_once_with(reconnect=False)
    assert result is connection


def test_test_connection_requires_connection(page):
    with pytest.raises(RuntimeError, match="No database connection"):
        page.test_connection()


def test_execute_script_ignores_blank_statements(page, connection):
    page.connection = connection
    cursor = connection.cursor.return_value.__enter__.return_value

    page._execute_script("  SELECT 1;\n; SELECT 2 ;; ")

    assert cursor.execute.call_args_list == [call("SELECT 1"), call("SELECT 2")]


def test_create_new_user_replaces_application_host(page, connection, monkeypatch):
    page.connection = connection
    page.host = "10.0.0.5"
    monkeypatch.setattr(
        "pathlib.Path.read_text",
        lambda *_args, **_kwargs: "CREATE USER 'app'@'{{ip}}';",
    )

    page.create_new_user()

    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.execute.assert_called_once_with("CREATE USER 'app'@'10.0.0.5'")
    connection.ping.assert_called_once_with(reconnect=False)


def test_migrate_data_rejects_invalid_database_name(page, monkeypatch):
    page.database_name.setText("legacy-db; DROP DATABASE darcoran")
    show_error = MagicMock()
    monkeypatch.setattr(page, "_show_error", show_error)

    assert page.migrate_data() is False
    show_error.assert_called_once_with("Enter a valid old database name.")


def test_migrate_data_runs_all_steps_and_substitutes_database(page, connection, monkeypatch):
    page.database_name.setText("legacy_db")
    page.connection = connection
    page.connect_to_database = MagicMock()
    page.create_new_database = MagicMock()
    page._execute_script = MagicMock()
    page.create_new_user = MagicMock()
    page.test_connection = MagicMock(return_value=True)
    monkeypatch.setattr(QMessageBox, "information", MagicMock())

    assert page.migrate_data() is True

    assert page.connect_to_database.call_args_list == [call(), call("darcoran"), call()]
    page.create_new_database.assert_called_once_with()
    page.create_new_user.assert_called_once_with()
    migration = page._execute_script.call_args.args[0]
    assert "from `legacy_db`.settings_money" in migration
    assert "{{old_db}}" not in migration
    connection.close.assert_called_once_with()
    assert page.connection is None


def test_migrate_data_rolls_back_and_reports_failures(page, connection, monkeypatch):
    page.database_name.setText("legacy_db")
    page.connection = connection
    page.connect_to_database = MagicMock(side_effect=RuntimeError("database down"))
    show_error = MagicMock()
    monkeypatch.setattr(page, "_show_error", show_error)

    assert page.migrate_data() is False

    show_error.assert_called_once_with("database down")
    connection.rollback.assert_called_once_with()
    connection.close.assert_called_once_with()
    assert page.connection is None