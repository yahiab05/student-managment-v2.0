from typing import overload, Literal

from .absents import AbsentStudent, AbsentTeacher
from .admin import Roles, Users
from .basic_operations import CRUD
from .classes import Classes, Enrollment
from .finance import Expense, Income
from .person import Student, StudentHistory, Teacher, TeacherHistory
from .settings import Settings

MODEL_REGISTRY = {
	"absent_student": AbsentStudent,
	"absent_students": AbsentStudent,
	"students_absent": AbsentStudent,
	"absent_teacher": AbsentTeacher,
	"absent_teachers": AbsentTeacher,
	"teachers_absent": AbsentTeacher,
	"classes": Classes,
	"enrollment": Enrollment,
	"enrollments": Enrollment,
	"expense": Expense,
	"expenses": Expense,
	"income": Income,
	"role": Roles,
	"roles": Roles,
	"settings": Settings,
	"student": Student,
	"students": Student,
	"student_history": StudentHistory,
	"students_history": StudentHistory,
	"teacher": Teacher,
	"teachers": Teacher,
	"teacher_history": TeacherHistory,
	"teachers_history": TeacherHistory,
	"user": Users,
	"users": Users,
}


class ModelFactory:
	"""Return the requested model helper from a single import surface."""

	def __new__(cls, session, model_name):
		key = str(model_name).strip().lower().replace(" ", "_")
		try:
			model_class = MODEL_REGISTRY[key]
		except KeyError as exc:
			available = ", ".join(sorted(MODEL_REGISTRY))
			raise ValueError(f"Unknown model '{model_name}'. Available models: {available}") from exc

		return model_class(session)

@overload
def get_model(session, 
            model_name: Literal[
                "absent_student", 
                "absent_students",
                "students_absent"]
            ) -> AbsentStudent: ...

@overload
def get_model(session,
            model_name: Literal[
                "absent_teacher",
                "absent_teachers",
                "teachers_absent"]
            ) -> AbsentTeacher: ...

@overload
def get_model(session,
            model_name: Literal[
                "enrollment",
                "enrollments"]
            ) -> Enrollment: ...

@overload
def get_model(session,
            model_name: Literal[
                "classes"]    
            ) -> Classes: ...

@overload
def get_model(session,
            model_name: Literal[
                "expense",
                "expenses"]
            ) -> Expense: ...

@overload
def get_model(session,
            model_name: Literal[
                "income"]
            ) -> Income: ...

@overload
def get_model(session,
            model_name: Literal[
                "role",
                "roles"]
            ) -> Roles: ...

@overload
def get_model(session,
            model_name: Literal[
                "settings"]
            ) -> Settings: ...

@overload
def get_model(session,
            model_name: Literal[
                "student",
                "students"]
            ) -> Student: ...

@overload
def get_model(session,
            model_name: Literal[
                "student_history",
                "students_history"]
            ) -> StudentHistory: ...

@overload
def get_model(session,
            model_name: Literal[
                "teacher",
                "teachers"]
            ) -> Teacher: ...

@overload
def get_model(session,
            model_name: Literal[
                "teacher_history",
                "teachers_history"]
            ) -> TeacherHistory: ...

@overload
def get_model(session,
            model_name: Literal[
                "user",
                "users"]
            ) -> Users: ...

def get_model(session, model_name):
	return ModelFactory(session, model_name)
