from ..repo.models import Classes as ClassesModel, ClassEleve as EnrollmentModel
from .basic_operations import CRUD


class Classes(CRUD):
    # Concrete child class for class records that uses the classes table.
    def __init__(self, session):
        super().__init__(session, ClassesModel)


class Enrollment(CRUD):
    # Concrete child class for enrollment records that uses the classeleve table.
    def __init__(self, session):
        super().__init__(session, EnrollmentModel)
