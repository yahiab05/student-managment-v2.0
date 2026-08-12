from enum import Enum

from app.view.base_table import BaseTable
from app.view.classes_tables import ClassesTableModel, ClasseleveTableModel
from app.view.finance_tables import (
	BalanceTableModel,
	EnteryTableModel,
	OutMoneyTableModel,
	PaymentTableModel,
	TransferTableModel,
)
from app.view.settings import ExpenseTypeTableModel, IncomeTypeTableModel
from app.view.students_tables import (
	StudentsHistoryTableModel,
	StudentsSearchTableModel,
	StudentsTableModel,
)
from app.view.teachers_tables import TeachersHistoryTableModel, TeachersTableModel, TeacherSearchTableModel


class TableType(str, Enum):
	CLASSES = "classes"
	CLASS_ENROLLMENT = "class_enrollment"
	STUDENTS = "students"
	STUDENT_HISTORY = "student_history"
	STUDENT_SEARCH = "student_search"
	TEACHERS = "teachers"
	TEACHER_HISTORY = "teacher_history"
	TEACHER_SEARCH = "teacher_search"
	INCOME_TYPES = "income_types"
	EXPENSE_TYPES = "expense_types"
	ENTRY = "entry"
	OUT_MONEY = "out_money"
	BALANCE = "balance"
	PAYMENT = "payment"
	TRANSFER = "transfer"


TABLE_MODEL_FACTORY = {
	TableType.CLASSES: ClassesTableModel,
	TableType.CLASS_ENROLLMENT: ClasseleveTableModel,
	TableType.STUDENTS: StudentsTableModel,
	TableType.STUDENT_HISTORY: StudentsHistoryTableModel,
	TableType.STUDENT_SEARCH: StudentsSearchTableModel,
	TableType.TEACHERS: TeachersTableModel,
	TableType.TEACHER_HISTORY: TeachersHistoryTableModel,
	TableType.TEACHER_SEARCH: TeacherSearchTableModel,
	TableType.INCOME_TYPES: IncomeTypeTableModel,
	TableType.EXPENSE_TYPES: ExpenseTypeTableModel,
	TableType.ENTRY: EnteryTableModel,
	TableType.OUT_MONEY: OutMoneyTableModel,
	TableType.BALANCE: BalanceTableModel,
	TableType.PAYMENT: PaymentTableModel,
	TableType.TRANSFER: TransferTableModel,
}


def create_table_model(table_type: TableType | str) -> BaseTable:
	if isinstance(table_type, str):
		table_type = TableType(table_type)

	try:
		table_model = TABLE_MODEL_FACTORY[table_type]
	except KeyError as exc:
		raise ValueError(f"Unknown table type: {table_type}") from exc

	return table_model()
