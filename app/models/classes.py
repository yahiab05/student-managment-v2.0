from ..repo.models import Classes as ClassesModel, ClassEleve as EnrollmentModel
from .basic_operations import CRUD


class Classes(CRUD):
    # Concrete child class for class records that uses the classes table.
    def __init__(self, session):
        super().__init__(session, ClassesModel)
        
    def get_filters(self, name=None, teacher=None):
        # Return a list of filters based on the provided name and teacher.
        filters = []
        if name:
            filters.append(self.db.table.name.ilike(f"%{name}%"))
        if teacher:
            filters.append(self.db.table.teacher.ilike(f"%{teacher}%"))
        return filters
        


class Enrollment(CRUD):
    # Concrete child class for enrollment records that uses the classeleve table.
    def __init__(self, session):
        super().__init__(session, EnrollmentModel)
