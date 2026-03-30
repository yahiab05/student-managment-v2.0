from .base_table import BaseTable
from PyQt6.QtCore import Qt

class TeachersTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "الاسم", "تاريخ التسجيل", "تاريخ الميلاد", "رقم الهاتف", "بمقابل", "المستخدم" ]

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.teachers[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.name
        elif column == 2:
            return class_obj.get_date_inscrit()
        elif column == 3:
            return class_obj.get_birthday()
        elif column == 4:
            return class_obj.phone
        elif column == 5:
            return class_obj.payed
        elif column == 6:
            return class_obj.note
        elif column == 7:
            return class_obj.user
        return None
    
class TeachersHistoryTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "الاسم", "سنوات التدريس", "تاريخ الميلاد", "بمقابل", "المستخدم" ]
        
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.teachers[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.teacher_id
        elif column == 1:
            return class_obj.teacher.name
        elif column == 2:
            return class_obj.get_date_inscrit()
        elif column == 3:
            return class_obj.teacher.get_birthday()
        elif column == 4:
            return class_obj.payed
        elif column == 5:
            return class_obj.user
        return None   
    
class TeacherSearchTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.teachers[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.name
        return None