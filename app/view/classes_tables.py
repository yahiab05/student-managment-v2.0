from .base_table import BaseTable
from PyQt6.QtCore import Qt

class ClassesTableModel(BaseTable):
    def __init__(self, session):
        super().__init__(session)
        
        self.headers = ["ID", "الاسم", "طريقة التدريس", "المعلم", "ملاحظة", "المبلغ", "مقابل", "عدد الحصص", "حصّة المعلم"]

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.classes[index.row()]
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
        elif column == 6:
            return class_obj.exchange
        elif column == 7:
            return class_obj.seance
        elif column == 8:
            return class_obj.teacher_part
        elif column == 9:
            return class_obj.user
        return None