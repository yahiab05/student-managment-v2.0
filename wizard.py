from mysql_wizard.core.setup import WizardPage
from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication([])
    wizard = WizardPage()
    wizard.show()
    app.exec()

