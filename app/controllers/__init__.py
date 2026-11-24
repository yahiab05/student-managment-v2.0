from app.controllers.login import Login
from app.controllers.config_controller import DBConfigLogic

from PyQt6.QtWidgets import QApplication
from app.repo.configs.db_configurer import DBConfig

def main():
    app = QApplication([])
    
    if not DBConfig().check_config_file_exists():
        window = DBConfigLogic()
    else:
        window = Login()
    
    window.show()
    app.exec()