from typing import overload, Literal

from app.repo.database import SessionLocal

from .admin import Roles, Users, Login
from .classes import Classes, Enrollment
from .finance import Expense, Income
from .person import Student, StudentHistory, Teacher, TeacherHistory
from .settings import Settings

MODEL_REGISTRY = {
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
def get_model(
			model_name: Literal[
				"enrollment",
				"enrollments"]
			) -> Enrollment: ...

@overload
def get_model(
			model_name: Literal[
				"classes"]    
			) -> Classes: ...

@overload
def get_model(
			model_name: Literal[
				"expense",
				"expenses"]
			) -> Expense: ...

@overload
def get_model(
			model_name: Literal[
				"income"]
			) -> Income: ...

@overload
def get_model(
			model_name: Literal[
				"role",
				"roles"]
			) -> Roles: ...

@overload
def get_model(
			model_name: Literal[
				"settings"]
			) -> Settings: ...

@overload
def get_model(
			model_name: Literal[
				"student",
				"students"]
			) -> Student: ...

@overload
def get_model(
			model_name: Literal[
				"student_history",
				"students_history"]
			) -> StudentHistory: ...

@overload
def get_model(
			model_name: Literal[
				"teacher",
				"teachers"]
			) -> Teacher: ...

@overload
def get_model(
			model_name: Literal[
				"teacher_history",
				"teachers_history"]
			) -> TeacherHistory: ...

@overload
def get_model(
			model_name: Literal[
				"user",
				"users"]
			) -> Users: ...

@overload
def get_model(
			model_name: Literal[
				"login"]
			) -> Login: ...

def get_model_list() -> list:
	"""Return a list of all available model classes."""
	return list(MODEL_REGISTRY.values())

def get_model(model_name):
	session = SessionLocal()
	return ModelFactory(session, model_name)

