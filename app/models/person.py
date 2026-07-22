
from .basic_operations import CRUD
from .classes import Enrollment
from ..utils.utils import error

class Student(CRUD):
    # Concrete child class for student records that uses the students table.
    def __init__(self, session):
        super().__init__(session, "students")
        self.enrollments = Enrollment(session)
        self.history = StudentHistory(session)
        
        self.set_static_metadata()
        
    def exists(self, name, parent):
        filters = [
            self.db.table.name == name,
            self.db.table.parent == parent
        ]
        verdict = self.exists(filters)

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
        return self.session.query(self.db.table).order_by(self.db.table.num_inscrit.desc()).first()

    def get_filters(self, name=None, gender=None, _from=None, _to=None, 
                    excused=None, activity=None):
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
    def __init__(self, session):
        super().__init__(session, Teachers)


class StudentHistory(CRUD):
    # Concrete child class for student history records that uses the students_history table.
    def __init__(self, session):
        super().__init__(session, "students_history")

    def set_date(self, date):
        return self.db.table.set_date_inscrit(date)
    

class TeacherHistory(CRUD):
    # Concrete child class for teacher history records that uses the teachershistory table.
    def __init__(self, session):
        super().__init__(session, TeachersHistoryModel)

