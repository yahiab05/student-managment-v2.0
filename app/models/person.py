
from ..repo.models import (
    Students,
    Teachers,
    StudentsHistory as StudentsHistoryModel,
    TeachersHistory as TeachersHistoryModel,
)
from .basic_operations import CRUD

class Student(CRUD):
    # Concrete child class for student records that uses the students table.
    def __init__(self, session):
        super().__init__(session, Students)


class Teacher(CRUD):
    # Concrete child class for teacher records that uses the teachers table.
    def __init__(self, session):
        super().__init__(session, Teachers)


class StudentHistory(CRUD):
    # Concrete child class for student history records that uses the students_history table.
    def __init__(self, session):
        super().__init__(session, StudentsHistoryModel)


class TeacherHistory(CRUD):
    # Concrete child class for teacher history records that uses the teachershistory table.
    def __init__(self, session):
        super().__init__(session, TeachersHistoryModel)

