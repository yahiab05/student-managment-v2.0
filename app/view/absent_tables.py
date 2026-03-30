from .base_table import BaseTable
from PyQt6.QtCore import Qt

class AbsentTeacherTableModel(BaseTable):
    def __init__(self, session):
        super().__init__(session)
        
        self.headers = ["ID", "الاسم", "القسم", "التاريخ", "من", "الى", "معوض", "تاريخ التعويض", "رقم الهاتف", "المستخدم"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            abs = self.rows[index.row()]
            if index.column() == 0:
                return abs.id
            elif index.column() == 1:
                return abs.teacher.name
            elif index.column() == 2:
                return abs.class_ab
            elif index.column() == 3:
                return abs.date_ab.strftime("%Y-%m-%d")
            elif index.column() == 4:
                return abs.du.strftime("%H:%M")
            elif index.column() == 5:
                return abs.time_last.strftime("%H:%M")
            elif index.column() == 6:
                return abs.rep
            elif index.column() == 7:
                return "" if abs.date_rep is None else abs.date_rep.strftime("%Y-%m-%d")
            elif index.column() == 8:
                return abs.teacher.phone
            elif index.column() == 9:
                return abs.user
        return None    
    
class AbsentStudentTableModel(BaseTable):
    def __init__(self, session):
        super().__init__(session)
        
        self.headers = ["ID", "الاسم", "القسم", "التاريخ", "من", "الى", "رقم الهاتف", "المستخدم"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            abs = self.rows[index.row()]
            if index.column() == 0:
                return abs.id
            elif index.column() == 1:
                return abs.student.name
            elif index.column() == 2:
                return abs.class_ab
            elif index.column() == 3:
                return abs.date_ab.strftime("%Y-%m-%d")
            elif index.column() == 4:
                return abs.du.strftime("%H:%M")
            elif index.column() == 5:
                return abs.time_last.strftime("%H:%M")
            elif index.column() == 6:
                return abs.student.num_tel
            elif index.column() == 7:
                return abs.user
        return None           