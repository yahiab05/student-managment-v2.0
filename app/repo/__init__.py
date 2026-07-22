from .facade import DBFacade
from .models import *


class Repositories:
    """Repository container that requires a SQLAlchemy `session` at creation.

    Use `get_repo(name)` to fetch a repository in O(1) time and minimal extra memory.
    """

    def __init__(self, session):
        self.session = session

        # Core entities
        self.roles = DBFacade(Role, session)
        self.users = DBFacade(Users, session)

        # Student related
        self.students = DBFacade(Students, session)
        self.students_history = DBFacade(StudentsHistory, session)

        # Teacher related
        self.teachers = DBFacade(Teachers, session)
        self.teachers_history = DBFacade(TeachersHistory, session)

        # Class related
        self.classes = DBFacade(Classes, session)
        self.classeleve = DBFacade(ClassEleve, session)

        # Financial entities
        self.income = DBFacade(Entery, session)
        self.expenses = DBFacade(OutMoney, session)

        # Settings and other
        self.settings = DBFacade(Settings, session)

        # Absence tracking
        self.teachers_absent = DBFacade(AbsentT, session)
        self.students_absent = DBFacade(AbsentS, session)

        # Lightweight name -> repo mapping for O(1) access without copying data
        self._map = {
            "roles": self.roles,
            "users": self.users,
            "students": self.students,
            "students_history": self.students_history,
            "teachers": self.teachers,
            "teachers_history": self.teachers_history,
            "classes": self.classes,
            "enrollments": self.classeleve,
            "income": self.income,
            "expenses": self.expenses,
            "settings": self.settings,
            "teachers_absent": self.teachers_absent,
            "students_absent": self.students_absent,
        }

    def get_repo(self, name: str):
        """Return the requested repository by name in O(1) time.

        This method uses a pre-built mapping of names to repository instances
        so lookups are constant time and do not allocate additional collections.
        """
        try:
            return self._map[name]
        except KeyError:
            raise KeyError(f"Unknown repository name: {name}")

    