from ..repo.models import Classes as ClassesModel, ClassEleve as EnrollmentModel
from .basic_operations import CRUD


class Classes(CRUD):
    # Concrete child class for class records that uses the classes table.
    def __init__(self, session):
        super().__init__(session, ClassesModel)
        self.set_static_metadata()
        
    def get_filters(self, name=None, teacher=None):
        # Return a list of filters based on the provided name and teacher.
        filters = []
        if name:
            filters.append(self.db.table.name.ilike(f"%{name}%"))
        if teacher:
            filters.append(self.db.table.teacher.ilike(f"%{teacher}%"))
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
    def __init__(self, session):
        super().__init__(session, EnrollmentModel)
