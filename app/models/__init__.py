from typing import Literal, overload

from app.repo.database import SessionLocal

from app.models.admin import Roles, Users, Login
from app.models.classes import Classes, Enrollment
from app.models.finance import Expense, Income
from app.models.person import Student, StudentHistory, Teacher, TeacherHistory
from app.models.settings import Settings
from app.models.names import ModelName

MODEL_REGISTRY = {
	ModelName.CLASSES: Classes,
	ModelName.ENROLLMENT: Enrollment,
	ModelName.ENROLLMENTS: Enrollment,
	ModelName.EXPENSE: Expense,
	ModelName.EXPENSES: Expense,
	ModelName.INCOME: Income,
	ModelName.ROLE: Roles,
	ModelName.ROLES: Roles,
	ModelName.SETTINGS: Settings,
	ModelName.STUDENT: Student,
	ModelName.STUDENTS: Student,
	ModelName.STUDENT_HISTORY: StudentHistory,
	ModelName.STUDENTS_HISTORY: StudentHistory,
	ModelName.TEACHER: Teacher,
	ModelName.TEACHERS: Teacher,
	ModelName.TEACHER_HISTORY: TeacherHistory,
	ModelName.TEACHERS_HISTORY: TeacherHistory,
	ModelName.USER: Users,
	ModelName.USERS: Users,
	ModelName.LOGIN: Login,
}


def _coerce_model_name(model_name: ModelName | str) -> ModelName:
	if isinstance(model_name, ModelName):
		return model_name

	normalized_name = str(model_name).strip().lower().replace(" ", "_")
	try:
		return ModelName(normalized_name)
	except ValueError as exc:
		available = ", ".join(member.value for member in ModelName)
		raise ValueError(f"Unknown model '{model_name}'. Available models: {available}") from exc


class ModelFactory:
	"""Return the requested model helper from a single import surface."""

	def __new__(cls, session, model_name: ModelName | str):
		key = _coerce_model_name(model_name)
		try:
			model_class = MODEL_REGISTRY[key]
		except KeyError as exc:
			available = ", ".join(member.value for member in MODEL_REGISTRY)
			raise ValueError(f"Unknown model '{model_name}'. Available models: {available}") from exc

		return model_class(session)

@overload
def get_model(
			model_name: Literal[
				ModelName.ENROLLMENT,
				ModelName.ENROLLMENTS]
			) -> Enrollment: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.CLASSES]
			) -> Classes: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.EXPENSE,
				ModelName.EXPENSES]
			) -> Expense: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.INCOME]
			) -> Income: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.ROLE,
				ModelName.ROLES]
			) -> Roles: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.SETTINGS]
			) -> Settings: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.STUDENT,
				ModelName.STUDENTS]
			) -> Student: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.STUDENT_HISTORY,
				ModelName.STUDENTS_HISTORY]
			) -> StudentHistory: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.TEACHER,
				ModelName.TEACHERS]
			) -> Teacher: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.TEACHER_HISTORY,
				ModelName.TEACHERS_HISTORY]
			) -> TeacherHistory: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.USER,
				ModelName.USERS]
			) -> Users: ...

@overload
def get_model(
			model_name: Literal[
				ModelName.LOGIN]
			) -> Login: ...

def get_model_list() -> list:
	"""Return a list of all available model classes."""
	return list(MODEL_REGISTRY.values())

def get_model(model_name: ModelName | str):
	session = SessionLocal()
	return ModelFactory(session, model_name)

