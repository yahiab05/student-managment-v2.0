from app.controllers.login import Login
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication([])
    window = Login()
    window.show()
    app.exec()