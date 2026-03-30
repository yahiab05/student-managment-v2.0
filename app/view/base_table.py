from PyQt6.QtCore import Qt, QAbstractTableModel
from abc import ABC, abstractmethod

class BaseTable(QAbstractTableModel, ABC):
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
    
    def refresh(self, new_data):
        self.beginResetModel()
        self.rows = new_data
        self.endResetModel()
        
    @abstractmethod
    def data(self, index, role): pass
