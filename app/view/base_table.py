from PyQt6.QtCore import Qt, QAbstractTableModel

class BaseTable(QAbstractTableModel):
    ID_COLUMN = 0
    
    def __init__(self):
        super().__init__()
                
        self.rows = []
        self.headers = []
                
    def rowCount(self, parent=None):
        return len(self.rows)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def headerData(self, section , orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None
    
    def refresh(self, new_data: list):
        self.beginResetModel()
        self.rows = new_data
        self.endResetModel()
        self.layoutChanged().emit()
        
    def get_current_data(self):
        return self.rows
        
    def data(self, index, role): 
        raise NotImplementedError("The data method must be implemented in the subclass.")
