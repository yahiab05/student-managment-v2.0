import os

import pytest
import pymysql
from PyQt6.QtWidgets import QMessageBox

from mysql_wizard.core.setup import WizardPage


pytestmark = pytest.mark.skipif(
    os.getenv("WIZARD_DB_INTEGRATION") != "1",
    reason="WIZARD_DB_INTEGRATION=1 is required",
)


@pytest.fixture
def database_connection():
    if os.getenv("WIZARD_DB_INTEGRATION") != "1":
        pytest.skip("WIZARD_DB_INTEGRATION=1 is required")
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DATABASE", "legacy_db"),
        autocommit=True,
    )


def test_seeded_legacy_database_contains_fixture(database_connection):
    with database_connection.cursor() as cursor:
        cursor.execute("SELECT name FROM students WHERE num_inscrit = 990001")
        assert cursor.fetchone()[0] == "CI Test Student"
    database_connection.close()


def test_wizard_migrates_seeded_legacy_database(qapp, monkeypatch):
    page = WizardPage()
    page.lineEdit.setText(os.getenv("MYSQL_DATABASE", "legacy_db"))
    page.host = os.getenv("MYSQL_HOST", "mysql")
    page.port = int(os.getenv("MYSQL_PORT", "3306"))
    page.root_user = os.getenv("MYSQL_USER", "root")
    page.root_password = os.getenv("MYSQL_PASSWORD", "root")
    monkeypatch.setattr(QMessageBox, "information", lambda *_args: None)
    monkeypatch.setattr(QMessageBox, "critical", lambda *_args: None)

    assert page.migrate_data() is True

    connection = pymysql.connect(
        host=page.host,
        port=page.port,
        user=page.root_user,
        password=page.root_password,
        database=page.database_name,
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM students WHERE name = 'CI Test Student'")
        assert cursor.fetchone()[0] == "CI Test Student"
    connection.close()