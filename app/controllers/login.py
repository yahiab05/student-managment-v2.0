from os import error, path
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.uic import loadUi
from app.repo import create_db
from app.models import ModelName, get_model

from app.controllers.mainWindow import mainWindow
from app.ui.ui_forms import LoginUI
from app.utils import set_username, load_gui, UiPath

class Login(QWidget, LoginUI):
    def __init__(self):
        create_db()  # Ensure the database is created before proceeding
        super().__init__()
        load_gui(UiPath.LOGIN, "login.ui", self)

        self.manager = get_model(ModelName.LOGIN)
        self.access_manager = get_model(ModelName.ACCESS)
        self.main_window = None  # Initialize main_window attribute
        
        self.setup()

    def setup(self):
        self.submit.clicked.connect(self.check_login)
    
    def check_login(self):
        username = self.username.text()
        password = self.password.text()
        login_checked, err_type = self.manager.check_login(username, password)
        if not login_checked:
            if err_type == 1:
                error("اسم المستخدم غير صحيح")
            elif err_type == 2:
                error("كلمة المرور غير صحيحة")
            return
        
        self.open_app(username)
            
    def open_app(self, user):
        set_username(user)
        self.set_access(user)
        self.main_window = mainWindow()

        self.main_window.show()
        
        self.close()  # Close the login window after opening the main application window
        
    def set_access(self, user):
        self.access_manager.set_user(user)
        self.access_manager.set_access()
        