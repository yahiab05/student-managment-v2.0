from pathlib import Path
import re

import pymysql
from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6.uic import loadUi


class WizardPage(QWidget):
    host = "localhost"
    port = 3306
    root_user = "root"
    root_password = "yahia"
    database_name = "darcoran"
    application_host = "localhost"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.connection = None
        self.connection_factory = pymysql.connect
        self.setup_ui()

    def setup_ui(self):
        ui_path = Path(__file__).resolve().parents[1] / "ui" / "wizard.ui"
        loadUi(str(ui_path), self)
        self.pushButton.clicked.connect(self.migrate_data)
    
    def create_new_database(self):
        if self.connection is None:
            self.connect_to_database()
            
        script_path = Path(__file__).resolve().parents[1] / "sql" / "structure.sql"
        script = script_path.read_text(encoding="utf-8")
        statements = [
            stmt.strip() for stmt in script.split(";") 
            if stmt.strip()
            ]

        with self.connection.cursor() as cursor:
            for statement in statements:
                if statement:
                    cursor.execute(
                        str(
                            statement
                        )
                    )
        self.test_connection()
    
    def connect_to_database(self, database=None):
        if self.connection is not None:
            self.connection.close()

        connection_args = {
            "host": self.host,
            "port": self.port,
            "user": self.root_user,
            "password": self.root_password,
            "autocommit": True,
        }
        if database is not None:
            connection_args["database"] = database

        self.connection = self.connection_factory(**connection_args)
        self.test_connection()
        return self.connection
    
    def test_connection(self, connection=None):
        connection = connection or self.connection
        if connection is None:
            raise RuntimeError("No database connection is available")
        connection.ping(reconnect=False)
        return True
    
    def migrate_data(self):
        old_db = self.lineEdit.text().strip()
        if not re.fullmatch(r"[A-Za-z0-9_$]+", old_db):
            self._show_error("Enter a valid old database name.")
            return False

        try:
            self.connect_to_database()
            self.create_new_database()
            self.connect_to_database(self.database_name)

            migration_path = Path(__file__).resolve().parents[1] / "sql" / "migration.sql"
            migration_sql = migration_path.read_text(encoding="utf-8")
            migration_sql = migration_sql.replace(
                "{{old_db}}", f"`{old_db.replace('`', '``')}`"
            )
            self._execute_script(migration_sql)
            self.test_connection()

            self.connect_to_database()
            self.create_new_user()
            self.test_connection()
        except Exception as error:
            self._show_error(str(error))
            if self.connection is not None:
                self.connection.rollback()
            return False
        finally:
            if self.connection is not None:
                self.connection.close()
                self.connection = None

        QMessageBox.information(self, "Migration", "Migration completed successfully.")
        return True
    
    def create_new_user(self):
        if self.connection is None:
            self.connect_to_database()

        user_path = Path(__file__).resolve().parents[1] / "sql" / "user.sql"
        user_sql = user_path.read_text(encoding="utf-8").replace(
            "{{ip}}", self.application_host
        )
        self._execute_script(user_sql)
        self.test_connection()

    def _execute_script(self, script):
        with self.connection.cursor() as cursor:
            for statement in script.split(";"):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)

    def _show_error(self, message):
        QMessageBox.critical(self, "Database setup failed", message)