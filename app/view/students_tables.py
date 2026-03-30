from .base_table import BaseTable
from PyQt6.QtCore import Qt

class StudentsTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        

        self.headers = ["المعرف", "الاسم", "تاريخ التسجيل", "تاريخ الولادة", "الجنس", "الولي", "رقم الهاتف", "رقم الهوية",
                        "معفى", "نشاط", "ملاحظات", "المستخدم"]
                
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        obj = self.rows[index.row()]
        column = index.column()

        if column == 0:
            return obj.num_inscrit
        elif column == 1:
            return obj.name
        elif column == 2:
            return obj.get_date_inscrit()
        elif column == 3:
            return obj.get_birthday()
        elif column == 4:
            return obj.gender
        elif column == 5:
            return obj.parent
        elif column == 6:
            return obj.num_tel
        elif column == 7:
            return obj.cin
        elif column == 8:
            return obj.excused
        elif column == 9:
            return obj.activity
        elif column == 10:
            return obj.note
        elif column == 11:
            return obj.user
        return None
    
class StudentsHistoryTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "الاسم", "تاريخ التسجيل", "تاريخ الميلاد", "الولي", "رقم الهاتف", "المستخدم"]

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.students[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.num_inscrit
        elif column == 1:
            return class_obj.student.name
        elif column == 2:
            return class_obj.get_date_inscrit()
        elif column == 3:
            return class_obj.student.get_birthday()
        elif column == 4:
            return class_obj.student.parent
        elif column == 5:
            return class_obj.student.num_tel
        elif column == 6:
            return class_obj.user
        return None
    
class StudentsSearchTableModel(BaseTable):
    def __init__(self):
        super().__init__()

        self.headers = ["ID", "الاسم"]
        
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        student = self.rows[index.row()]
        column = index.column()

        if column == 0:
            return student.num_inscrit
        elif column == 1:
            return student.name