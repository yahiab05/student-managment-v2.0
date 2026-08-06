from os import path
from PyQt6.uic import loadUi

class mainWindow:
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        ui_path = path.abspath("../ui/mainWindow.ui")
        loadUi(ui_path, self)