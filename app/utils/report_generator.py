from xlsxwriter import Workbook, exceptions
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from os import path
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from jinja2 import Template
    
class ExcelGenerator:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data
        
    def excel(self, file):
        try:
            book = Workbook(file[0])
            sheet = book.add_worksheet("dataimported")

            # initialize rows and columns of the worksheet
            row = 0
            col = 0

            # Insert the columns name in to the excel
            for heading in self.headers:
                sheet.write(row, col, heading)
                col += 1
            # Create a For loop to iterate through each entries in the db file
            for entry in self.data:
                row += 1
                col = 0
                for data_val in entry:
                    sheet.write(row, col, data_val)
                    col += 1

            book.close()
        except exceptions.FileCreateError:
            pass


class Printing(QDialog):
    def __init__(self):
        super().__init__()

        ui_path = path.abspath("../dar coran(new)/ui/printing.ui")  # Convert to absolute path
        loadUi(ui_path, self)

        self.adapt_size()

        self.setup()

    def setup(self):
        self.printing.clicked.connect(self.print_file)
        self.cancel.clicked.connect(self.canceled)

    def adapt_size(self):
        """Resizes the QDialog based on screen height."""
        screen = QApplication.primaryScreen().geometry()  # Get screen size
        screen_height = screen.height()  # Get screen height
        self.setMinimumHeight(int(screen_height * 0.6))  # Set height to 60% of screen
        self.setMaximumHeight(int(screen_height * 0.9))  # Max height is 90% of screen

    def setup_document(self, data, headers, title="", intro="", foot=""):
        self.printing_plain.clear()
        self.printing_plain.setFontPointSize(20)
        self.printing_plain.append(title)
        self.printing_plain.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.printing_plain.append("""   """)
        self.printing_plain.setFontPointSize(12)
        self.printing_plain.append(intro)
        self.printing_plain.append("""   """)
        table = """
                        <style>
                        table {
                            font-family: arial, sans-serif;
                            border-collapse: collapse;
                            width: 100%;
                        }

                        td, th {
                            border: 1px solid #dddddd;
                            text-align: center;
                            padding: 4px;
                        }
                        </style>

                        <table border="1" width="100%">
                            <tr>{% for header in headers %}<th>{{header}}</th>{% endfor %}</tr>
                            {% for row in rows %}<tr>
                                {% for element in row %}<td>
                                    {{element}}
                                </td>{% endfor %}
                            </tr>{% endfor %}
                        </table>
                        """
        self.printing_plain.append(Template(table).render(headers=headers, rows=data))
        self.printing_plain.append("""  """)
        self.printing_plain.setFontPointSize(12)
        self.printing_plain.append(foot)
        self.printing_plain.setAlignment(Qt.AlignmentFlag.AlignLeft)


    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.printing_plain.print(printer)
            self.canceled()

    def canceled(self):
        self.close()