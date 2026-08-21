from os import path
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
        
        # for development purposes, pre-fill the username and password fields
        self.username.setText("yahia")
        self.password.setText("123")

        self.manager = get_model(ModelName.LOGIN)
        self.access_manager = get_model(ModelName.ACCESS)
        
        self.setup()

    def setup(self):
        self.submit.clicked.connect(self.check_login)
    
    def check_login(self):
        username = self.username.text()
        password = self.password.text()
        login_checked = self.manager.check_login(username, password)
        print(f"Login checked: {login_checked} for user: {username}")
        if login_checked:
            self.open_app(username)
            
    def open_app(self, user):
        set_username(user)
        self.set_access(user)
        app = QApplication.instance()  # Get the existing QApplication instance
        if app is None:
            app = QApplication([])  # Create a new QApplication if it doesn't exist
        app.main_window = mainWindow()
        app.main_window.show()
        
        self.close()  # Close the login window after opening the main application window
        
    def set_access(self, user):
        self.access_manager.set_user(user)
        self.access_manager.set_access()
        