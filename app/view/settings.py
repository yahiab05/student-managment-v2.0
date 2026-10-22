from app.view.base_table import BaseTable
from PyQt6.QtCore import Qt

class IncomeTypeTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "Nom", "code"]
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.rows[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.entry
        elif column == 2:
            return class_obj.entry_code
        return None
    
class ExpenseTypeTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        self.headers = ["ID", "Nom", "code"]
        
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.rows[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.out
        elif column == 2:
            return class_obj.out_code
        return None