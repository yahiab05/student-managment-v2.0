import gc
from os import environ, getenv, path
from pathlib import Path
from subprocess import run
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from app.ui.ui_forms import MainUI
from app.controllers.controller_factory import ControllerFactory, ControllerSection

class mainWindow(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        ui_path = path.abspath(path.join(path.dirname(__file__), "..", "ui", "main.ui"))
        loadUi(ui_path, self)
        
        buttons = {
            ControllerSection.ADMIN: self.user,
            ControllerSection.CLASSES: self.classes,
            ControllerSection.TEACHERS: self.teachers,
            ControllerSection.PAYMENTS: self.payment,
            ControllerSection.SETTINGS: self.settings,
            ControllerSection.STUDENTS: self.students,
            ControllerSection.FINANCE: self.money
        }
        
        self.factory = ControllerFactory()
        self.factory.setup_sections(self.stackedWidget, buttons)
        
    def closeEvent(self, event):
        ret = QMessageBox.question(self, 'حفظ', "متأكد من حفظ المعطيات؟", 
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if ret == QMessageBox.StandardButton.Yes:
            self.backup_mysql_db()
        gc.collect()
        event.accept()
        
    def backup_mysql_db(self) -> str:
        backup_dir = QFileDialog.getExistingDirectory(self, 
                                                    'Select Directory',
                                                    '',
                                                    QFileDialog.Option.ShowDirsOnly)
        
        database = getenv("MYSQL_DATABASE")
        password = getenv("MYSQL_PWD")
        host = getenv("MYSQL_HOST")
        port = getenv("MYSQL_PORT")
        user = getenv("MYSQL_USER")
        
        if not backup_dir:
            return None
        backup_path = Path(backup_dir)
        

        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        out_file = backup_path / f"{database}_{stamp}.sql"

        # Use env var for password to avoid showing it in process list
        env = environ.copy()
        env["MYSQL_PWD"] = password

        if not all([database, password, host, port, user]):
            print("database: ", database)
            print("password: ", password)
            print("host: ", host)
            print("port: ", port)
            print("user: ", user)
            
            raise ValueError("Missing database environment variables")
        cmd = [
            "mysqldump",
            "-h", host,
            "-P", str(port),
            "-u", user,
            "--routines",
            "--triggers",
            "--single-transaction",
            "--databases", database,
        ]

        with out_file.open("wb") as f:
            result = run(cmd, stdout=f, stderr=subprocess.PIPE, env=env)

        if result.returncode != 0:
            # Clean partial dump if failed
            try:
                out_file.unlink(missing_ok=True)
            except Exception:
                pass
            raise RuntimeError(f"mysqldump failed: {result.stderr.decode('utf-8', errors='replace')}")

        return str(out_file)