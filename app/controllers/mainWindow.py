import gc
from os import environ, getenv
from pathlib import Path
from subprocess import PIPE, run
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QStackedWidget, QWidget
from app.ui.ui_forms import MainUI
from app.controllers.controller_factory import ControllerFactory, ControllerSection
from app.models import get_model, ModelName
from app.utils import load_gui, UiPath, get_combo_manager, get_username
from app.repo import configs

class mainWindow(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        load_gui(UiPath.MAIN, "main.ui", self)
        
        buttons = {
            ControllerSection.ADMIN: self.user,
            ControllerSection.CLASSES: self.classes,
            ControllerSection.TEACHERS: self.teachers,
            ControllerSection.PAYMENTS: self.payment,
            ControllerSection.SETTINGS: self.settings,
            ControllerSection.STUDENTS: self.students,
            ControllerSection.FINANCE: self.money
        }
        
        self.showMaximized()
        self.combo_manager = get_combo_manager
        self.combo_manager.update_all_cache()
        
        self.factory = ControllerFactory()
        self.factory.setup_sections(self.stackedWidget, buttons)
        
        self.access_manager = get_model(ModelName.ACCESS)
        
        self.username.setText(get_username())
        
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
        
        database = configs.name
        password = configs.password
        host = configs.host
        port = configs.port
        user = configs.user
        
        if not backup_dir:
            return None
        backup_path = Path(backup_dir)
        

        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        out_file = backup_path / f"{database}_{stamp}.sql"

        # Use env var for password to avoid showing it in process list
        env = environ.copy()
        env["MYSQL_PWD"] = password
            
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
            try:
                result = run(cmd, stdout=f, stderr=PIPE, env=env)
            except Exception as e:
                raise RuntimeError(f"mysqldump failed: {str(e)}")
        if result.returncode != 0:
            # Clean partial dump if failed
            try:
                out_file.unlink(missing_ok=True)
            except Exception:
                pass
            raise RuntimeError(f"mysqldump failed: {result.stderr.decode('utf-8', errors='replace')}")

        return str(out_file)
    
    def access_control(self):
        self.students.setEnabled(self.access_manager.get_access("students"))
        self.classes.setEnabled(self.access_manager.get_access("classes"))
        self.teachers.setEnabled(self.access_manager.get_access("teachers"))
        self.payment.setEnabled(self.access_manager.get_access("payment"))
        self.money.setEnabled(self.access_manager.get_access("money"))
        self.settings.setEnabled(self.access_manager.get_access("settings"))
        self.user.setEnabled(self.access_manager.get_access("user"))
        
if __name__ == '__main__':
    app = QApplication([])
    window = mainWindow()
    window.show()
    app.exec()