from ..repo.models import AbsentT as AbsentTeacherModel, AbsentS as AbsentStudentModel
from .basic_operations import CRUD


class AbsentTeacher(CRUD):
    # Concrete child class for teacher absence records that uses the absent_t table.
    def __init__(self, session):
        super().__init__(session, AbsentTeacherModel)


class AbsentStudent(CRUD):
    # Concrete child class for student absence records that uses the absent_s table.
    def __init__(self, session):
        super().__init__(session, AbsentStudentModel)
