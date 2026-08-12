from os import path

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget
from app.ui.ui_forms import PopupFormUI
from PyQt6.QtCore import pyqtSignal
from app.controllers.popup.dynamic_windows import FormProtocol

class BaseWindow(QWidget, PopupFormUI):
    confirmed = pyqtSignal()
    
    def __init__(self, title:str, content:FormProtocol, parent=None):
        super().__init__(parent)
        self.title_content = title
        self.content = content
        self.setup_ui()

    def setup_ui(self):
        # Load the UI file for the base window
        ui_path = path.abspath(path.join(path.dirname(__file__), "..", "..", "ui", "forms", "popup_form.ui"))
        loadUi(ui_path, self)
        
        self.title.setText(self.title_content)
        self.widget.layout().addWidget(self.content)
        
        self.confirm_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
    def accept(self):
        self.confirmed.emit()
        self.close()
        
    def reject(self):
        self.close()