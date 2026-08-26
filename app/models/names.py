from enum import StrEnum, auto


class ModelName(StrEnum):
	CLASSES = auto()
	ENROLLMENT = ENROLLMENTS = "enrollments"
	EXPENSE = EXPENSES = "expenses"
	PAYMENTS = INCOME = "income"
	ROLE = ROLES = "roles"
	SETTINGS = auto()
	STUDENT = STUDENTS = "students"
	STUDENT_HISTORY = STUDENTS_HISTORY = "students_history"
	TEACHER = TEACHERS = "teachers"
	TEACHER_HISTORY = TEACHERS_HISTORY = "teacher_history"
	LOGIN = USER = USERS = "users"
	BALANCE = auto()
	TRANSFER = auto()
	ACCESS = auto()
