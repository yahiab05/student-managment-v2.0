from ..models import get_model
from PyQt6.uic import loadUi
from ..repo import create_db

from .mainWindow import mainWindow

class Login:
    def __init__(self):
        
        create_db()  # Ensure the database is created before proceeding

        path = path.abspath("../ui/login.ui")

        loadUi(path, self)
        
        self.manager = get_model("login")

    def setup(self):
        self.submit.clicked.connect(self.check_login)
    
    def check_login(self):
        username = self.username.text()
        password = self.password.text()
        login_checked = self.manager.check_login(username, password)
        
        if login_checked:
            self.open_app(username)
            
    def open_app(self, user):
        main_window = mainWindow(user)
        main_window.show()
        
        self.close()  # Close the login window after opening the main application window
        