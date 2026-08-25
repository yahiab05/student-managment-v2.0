from PyQt6.QtWidgets import QDialog, QVBoxLayout
from app.ui.ui_forms import PopupFormUI
from PyQt6.QtCore import pyqtSignal
from app.controllers.popup.dynamic_windows import FormProtocol
from app.utils import load_gui, UiPath

class BaseWindow(QDialog, PopupFormUI):
    confirmed = pyqtSignal()
    
    def __init__(self, title:str, content:FormProtocol, parent=None):
        super().__init__(parent)
        self.title_content = title
        self.content = content
        self.setup_ui()

    def setup_ui(self):
        # Load the UI file for the base window
        load_gui(UiPath.FORMS, "popup_form.ui", self)
        
        self.title.setText(self.title_content)
        layout = QVBoxLayout(self.widget)
        layout.addWidget(self.content)

        self.confirm_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
    def accept(self):
        self.confirmed.emit()
        self.close()
        
    def reject(self):
        self.close()