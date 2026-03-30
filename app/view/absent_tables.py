from .base_table import BaseTable
from PyQt6.QtCore import Qt

class AbsentTeacherTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "الاسم", "القسم", "التاريخ", "من", "الى", "معوض", "تاريخ التعويض", "رقم الهاتف", "المستخدم"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        
        column = index.column()
        abs = self.rows[index.row()]
        
        if column == 0:
            return abs.id
        elif column == 1:
            return abs.teacher.name
        elif column == 2:
            return abs.class_ab
        elif column == 3:
            return abs.date_ab.strftime("%Y-%m-%d")
        elif column == 4:
            return abs.du.strftime("%H:%M")
        elif column == 5:
            return abs.time_last.strftime("%H:%M")
        elif column == 6:
            return abs.rep
        elif column == 7:
            return "" if abs.date_rep is None else abs.date_rep.strftime("%Y-%m-%d")
        elif column == 8:
            return abs.teacher.phone
        elif column == 9:
            return abs.user
        return None    
    
class AbsentStudentTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "الاسم", "القسم", "التاريخ", "من", "الى", "رقم الهاتف", "المستخدم"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        abs = self.rows[index.row()]
        column = index.column()
        if column == 0:
            return abs.id
        elif column == 1:
            return abs.student.name
        elif column == 2:
            return abs.class_ab
        elif column == 3:
            return abs.date_ab.strftime("%Y-%m-%d")
        elif column == 4:
            return abs.du.strftime("%H:%M")
        elif column == 5:
            return abs.time_last.strftime("%H:%M")
        elif column == 6:
            return abs.student.num_tel
        elif column == 7:
            return abs.user
        return None           