from PyQt6.QtWidgets import QWidget

from app.utils import  load_gui, UiPath
from app.ui.ui_forms import DBConfigUI
from app.repo.configs.db_configurer import DBConfig
from pymysql import connect, MySQLError

class DBConfigLogic(QWidget, DBConfigUI):
    def __init__(self, parent = None):
        super().__init__(parent)

        load_gui(UiPath.OTHERS, "db_config.ui", self)

    def setup(self):
        self.test_btn.clicked.connect(self.test_connection)
        self.confirm_btn.clicked.connect(self.confirm_config)
        
    def test_connection(self):
        configurer = DBConfig()
        if not configurer.check_config_file_exists():
            raise FileNotFoundError(f"Configuration file not found: {configurer.path}. Please ensure the file exists and is readable.")
        
        configs = configurer.get_configuration()
        
        try:
            connection = connect(
                host=configs.host,
                port=configs.port,
                user=configs.user,
                password=configs.password,
                database=configs.name,
                connect_timeout=5
            )

            connection.close()
            return True

        except MySQLError as e:
            print(f"MySQL connection failed: {e}")
            return False
        
    def confirm_config(self):
        configurer = DBConfig()
        if not configurer.check_config_file_exists():
            raise FileNotFoundError(f"Configuration file not found: {configurer.path}. Please ensure the file exists and is readable.")
        
        configs = configurer.get_configuration()
        
        if self.test_connection():
            print("Database connection successful. Configuration confirmed.")
            # You can add additional logic here to proceed with the application flow
        
        else:
            print("Database connection failed. Please check your configuration.")