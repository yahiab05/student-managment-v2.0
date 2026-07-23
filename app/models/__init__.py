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


def get_model(session, model_name):
	return ModelFactory(session, model_name)


__all__ = [
	"CRUD",
	"AbsentStudent",
	"AbsentTeacher",
	"Classes",
	"Enrollment",
	"Expense",
	"Income",
	"ModelFactory",
	"MODEL_REGISTRY",
	"Roles",
	"Settings",
	"Student",
	"StudentHistory",
	"Teacher",
	"TeacherHistory",
	"Users",
	"get_model",
]
