from PyQt6.QtWidgets import QApplication, QWidget

from app.controllers.login import Login
from app.utils import  load_gui, UiPath
from app.ui.ui_forms import DBConfigUI
from app.repo.configs.db_configurer import DBConfig
from pymysql import connect, MySQLError
from app.utils import error, info

class DBConfigLogic(QWidget, DBConfigUI):
    def __init__(self, parent = None):
        super().__init__(parent)

        load_gui(UiPath.OTHERS, "db_config.ui", self)
        self.setup()
        
        self.login_window = None

    def setup(self):
        self.test_btn.clicked.connect(self.test_connection)
        self.confirm_btn.clicked.connect(self.confirm_config)
        
    def test_connection(self):
        host = self.ip.text()
        pwd = self.password.text()
        
        try:
            connection = connect(
                host=str(host),
                port=3306,
                user="darcoran_app",
                password=str(pwd),
                database="darcoran",
                connect_timeout=5
            )

            connection.close()
            info("Database connection successful.")
            return True

        except MySQLError as e:
            error(f"MySQL connection failed: {e}")
            return False

    def confirm_config(self):
        if not self.test_connection():
            return
        configurer = DBConfig()
        configurer.create_config_file(host=self.ip.text(), password=self.password.text())
        info(f"Database configuration saved to {configurer.path}.")
        
        self._load_app()
        
    def _load_app(self):
        self.login_window = Login()
        self.login_window.show()
        
        self.close()