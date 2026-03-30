from PyQt6.QtCore import Qt, QAbstractTableModel

class BaseTable(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session
        
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
    
    def refresh(self, new_data):
        self.beginResetModel()
        self.rows = new_data
        self.endResetModel()
