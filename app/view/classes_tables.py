from .base_table import BaseTable
from PyQt6.QtCore import Qt

class ClassesTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "الاسم", "طريقة التدريس", "المعلم", "ملاحظة", "المبلغ", "مقابل", "عدد الحصص", "حصّة المعلم", "المستخدم"]

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.rows[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.name
        elif column == 2:
            return class_obj.way
        elif column == 3:
            return class_obj.teacher
        elif column == 4:
            return class_obj.note
        elif column == 5:
            return class_obj.price
        elif column == 9:
            return class_obj.user
        return None
    
class ClasseleveTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "الاسم", "رقم التسجيل", "القسم", "تاريخ آلتسجيل", "تاريخ الميلاد", "رقم الهاتف", "المستخدم"]
        
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.rows[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.student.name
        elif column == 2:
            return class_obj.student_id
        elif column == 3:
            return class_obj.class_name
        elif column == 4:
            item = class_obj.student.date_inscrit
            return item.strftime("%Y-%m-%d") if item else ""
        elif column == 5:
            item = class_obj.student.birthday
            return item.strftime("%Y-%m-%d") if item else ""
        elif column == 6:
            return class_obj.student.num_tel
        elif column == 7:
            return class_obj.user
        return None