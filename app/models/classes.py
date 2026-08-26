from app.models.names import ModelName
from app.models.basic_operations import CRUD


class Classes(CRUD):
    # Concrete child class for class records that uses the classes table.
    def __init__(self):
        super().__init__(ModelName.CLASSES)
        self.set_static_metadata()
        
    def get_filters(self, name=None, teacher=None, way_teaching= None, exact_teacher=None):
        # Return a list of filters based on the provided name and teacher.
        filters = []
        if name:
            filters.append(self.db.table.name.ilike(f"%{name}%"))
        if teacher:
            filters.append(self.db.table.teacher.ilike(f"%{teacher}%"))
        if exact_teacher:
            filters.append(self.db.table.teacher == exact_teacher)
        if way_teaching:
            filters.append(self.db.table.way_teaching == way_teaching)
        return filters
    
    def set_static_metadata(self):
        self.title = "قائمة الأقسام"

        self.headers = ["الثمن", "الأستاذ", "الطريقة", "الإسم"]

    def set_dynamic_metadata(self, data_to_export, row_count):
        self.foot = f"""عدد الأقسام: {row_count}"""

        for class_ in data_to_export:
            row = [
                str(class_.price),
                class_.teacher,
                class_.way,
                class_.name
            ]
            self.data_to_export.append(row)

class Enrollment(CRUD):
    # Concrete child class for enrollment records that uses the classeleve table.
    def __init__(self):
        super().__init__(ModelName.ENROLLMENTS)
        self.set_static_metadata()
        
    def check(self, student_id, class_name):        
        verdict = self.exists(
            [ self.db.table.student_id == student_id, 
            self.db.table.class_name == class_name]
            )
        
        return verdict
    
    def get_filters(self, class_name=None, student_id=None, not_class_name=None, not_included:list=None):
        # Return a list of filters based on the provided class_name.
        filters = []
        if class_name:
            filters.append(self.db.table.class_name == class_name)
        if student_id:
            filters.append(self.db.table.student_id == student_id)
        if not_class_name:
            filters.append(self.db.table.class_name != not_class_name)
        if not_included:
            filters.append(self.db.table.student_id.not_in(not_included))
        return filters

    def set_static_metadata(self):
        self.title = "قائمة التلاميذ"
        self.headers = ["رقم الهاتف", "تاريخ الولادة", "رقم الترسيم", "السيد(ة)"]

    def set_dynamic_metadata(self, data_to_export, row_count, class_name, teacher):
        self.foot = f"عدد التلاميذ: {row_count}"
        
        self.intro = ""
        if class_name:
            self.intro = f"{class_name}\n"
        if teacher:
            self.intro += f"اسم المعلم: {teacher}"

        self.data_to_export = []
        for student in data_to_export:
            row = [
                str(student.student_id.num_tel),
                student.student_id.birthday.strftime("%Y-%m-%d"),
                str(student.student_id),
                student.student.name,
            ]
            self.data_to_export.append(row)
        
        
