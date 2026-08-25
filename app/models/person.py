from app.models.names import ModelName
from app.models.basic_operations import CRUD
from app.models.classes import Enrollment
from app.utils.utils import error

class Student(CRUD):
    # Concrete child class for student records that uses the students table.
    def __init__(self):
        super().__init__(ModelName.STUDENTS)
        self.enrollments = Enrollment()
        self.history = StudentHistory()
        
        self.set_static_metadata()
        
    def exists(self, name, parent):
        filters = [
            self.db.table.name == name,
            self.db.table.parent == parent
        ]
        verdict = self.db.exists(filters)

        return verdict
    
    def delete(self, id):
        if self.permenant(id):
            super().delete(id)
        else:
            self.deactivate(id)
            
    def deactivate(self, id):
        filters = self.enrollments.get_filters(
            student_id=id,
            not_class_name="تأمين"
        )
        enrollments = self.enrollments.get_by_filter(filters)
        if len(enrollments) > 0:
            error("لا يمكن حذف هذا الشخص لأنه مرتبط ببيانات أخرى في النظام.")
            return
        
        student = self.get_by_id(id)
        if student is not None:
            student.activity = "غير فاعل"
            self.db.commit()

    def permenant(self, id):
        
        student = self.get_by_id(id)
        if student is not None:
            return student.activity == "غير فاعل"
        
        return False
                
    def get_last_student(self):
        return self.db.get_biggest_id()

    def get_filters(self, name=None, gender=None, _from=None, _to=None, 
                    excused=None, activity=None, not_included: list=None):
        # Return a list of filters based on the provided name and gender.
        filters = []
        self.intro = ""
        
        if name:
            filters.append(self.db.table.name.ilike(f"%{name}%"))

        if _from and _to:
            filters.append(self.db.table.date_inscrit >= self.history.set_date(_from))
            filters.append(self.db.table.date_inscrit <= self.history.set_date(_to))
            self.intro = """ بين  """ + _from.strftime("%Y-%m-%d") + "  و  " + _to.strftime("%Y-%m-%d") + "\n"
        if excused:
            filters.append(self.db.table.excused == excused)
            self.intro += "معفى: " + excused + "\n"
        if activity:
            filters.append(self.db.table.activity == activity)
            self.intro += "نشاط: " + activity
        if gender:
            filters.append(self.db.table.gender == gender)
            self.intro += "جنس: " + gender
        if not_included:
            filters.append(self.db.table.num_inscrit.not_in(not_included))
        return filters
    
    def set_static_metadata(self):
        self.title = "قائمة التلميذ"

        self.header = ["معفى", "رقم الهاتف", "تاريخ الولادة", "الإسم"]
            
    def set_dynamic_metadata(self, data_to_export, row_count):
        self.foot = f"عدد التلاميذ: {row_count}"
        self.data_to_export = []
        for student in data_to_export:
            row = [
                student.excused,
                str(student.num_tel),
                student.birthday.strftime("%Y-%m-%d"),
                student.name
            ]
            self.data_to_export.append(row)
class Teacher(CRUD):
    # Concrete child class for teacher records that uses the teachers table.
    def __init__(self):
        super().__init__(ModelName.TEACHERS)
        
        self.set_static_metadata()
        
    def get_filters(self, name=None):
        filters = []
        if name is not None:
            filters.append(self.db.table.name.ilike(f"%{name}%"))
            
        return filters
    
    def set_static_metadata(self):
        self.title = "قائمة الأساتذة"

        self.header = ["رقم الهاتف", "تاريخ الولادة", "الإسم"]

    def set_dynamic_metadata(self, data_to_export, row_count):
        self.foot = "المجموع: " + str(row_count)
        self.data_to_export = data_to_export
        
    def get_last_id(self):
        return self.db.get_biggest_id() 

class StudentHistory(CRUD):
    # Concrete child class for student history records that uses the students_history table.
    def __init__(self):
        super().__init__(ModelName.STUDENTS_HISTORY)

    def search_by_num_inscrit(self, num_inscrit: int):
        """Search history records by student number, joined with the student table."""

        filters = [self.db.table.id == num_inscrit]
        return self.get_with_joined_load("student", filters)

    def set_static_metadata(self):
        self.title = "قائمة التلميذ"
        self.header = ["معفى", "رقم الهاتف", 'سنوات الدراسة', "تاريخ الولادة", "الإسم"]

    def set_dynamic_metadata(self, data_to_export, row_count):
        self.data_to_export = data_to_export
        self.foot = "المجموع: " + str(row_count)
        self.intro = "تلميذ برقم الهوية: " + str(self.data_to_export[0].id) if self.data_to_export else "تلميذ غير موجود"


class TeacherHistory(CRUD):
    # Concrete child class for teacher history records that uses the teachershistory table.
    def __init__(self):
        super().__init__(ModelName.TEACHERS_HISTORY)

    def search_by_id(self, teacher_id: int):
        """Search history records by teacher ID, joined with the teacher table."""

        filters = [self.db.table.teacher_id == teacher_id]
        return self.get_with_joined_load("teacher", filters)
    
    def set_static_metadata(self):
        self.title = "قائمة الأساتذة"

        self.headers = ["تاريخ الولادة", "سنوات التدريس", "الإسم", "رقم التسجيل"]

    def set_dynamic_metadata(self, data_to_export, row_count):
        self.foot = f"""عدد الأساتذة: {row_count}"""
        self.data_to_export = data_to_export
