from app.repo.facade import DBFacade, BalanceFacade
from app.repo.models import *
from app.repo.database import create_db, SessionLocal, configs

class Repositories:
    """Repository container that requires a SQLAlchemy `session` at creation.

    Use `get_repo(name)` to fetch a repository in O(1) time and minimal extra memory.
    """

    def __init__(self):
        # Core entities
        self.roles = DBFacade(Role)
        self.users = DBFacade(Users)

        # Student related
        self.students = DBFacade(Students)
        self.students_history = DBFacade(StudentsHistory)

        # Teacher related
        self.teachers = DBFacade(Teachers)
        self.teachers_history = DBFacade(TeachersHistory)

        # Class related
        self.classes = DBFacade(Classes)
        self.classeleve = DBFacade(ClassEleve)

        # Financial entities
        self.income = DBFacade(Entery)
        self.expenses = DBFacade(OutMoney)
        self.balance = BalanceFacade()  # Specialized facade for combined financial queries
        self.transfer = DBFacade(Transfer)

        # Settings and other
        self.settings = DBFacade(Settings)

        # Lightweight name -> repo mapping for O(1) access without copying data
        self._map = {
            "roles": self.roles,
            "users": self.users,
            "students": self.students,
            "students_history": self.students_history,
            "teachers": self.teachers,
            "teacher_history": self.teachers_history,
            "classes": self.classes,
            "enrollments": self.classeleve,
            "income": self.income,
            "expenses": self.expenses,
            "settings": self.settings,
            "balance": self.balance,
            "transfer": self.transfer
        }

    def get_repo(self, name: str) -> DBFacade:
        """Return the requested repository by name in O(1) time.

        This method uses a pre-built mapping of names to repository instances
        so lookups are constant time and do not allocate additional collections.
        """
        try:
            return self._map[name] if name in self._map and name != "balance" else None
        except KeyError:
            raise KeyError(f"Unknown repository name: {name}")
        
    def get_balance_repo(self) -> BalanceFacade:
        """Return the specialized balance repository for combined financial queries."""
        return self.balance

    