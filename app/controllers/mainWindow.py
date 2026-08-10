from os import path
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
from ..ui.ui_forms import MainUI

class mainWindow(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        ui_path = path.abspath(path.join(path.dirname(__file__), "..", "ui", "main.ui"))
        loadUi(ui_path, self)