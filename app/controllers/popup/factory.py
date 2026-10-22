from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable

from app.controllers.popup.base_window import BaseWindow
from app.controllers.popup.dynamic_windows import (
    ClassesForm,
    ExpensesForm,
    IncomeForm,
    StudentForm,
    TeacherForm,
    PaymentForm
)


class PopupKind(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    CLASSES = "classes"
    EXPENSES = "expenses"
    INCOME = "income"


@runtime_checkable
class PopupContentProtocol(Protocol):
    def get_data(self) -> dict: ...


@runtime_checkable
class PopupFactoryProtocol(Protocol):
    def _create_content(self, kind: PopupKind, parent=None) -> PopupContentProtocol: ...

    def create_window(self, kind: PopupKind, title: str, parent=None) -> BaseWindow: ...


class PopupFactory(PopupFactoryProtocol):
    _content_map = {
        PopupKind.STUDENT: StudentForm,
        PopupKind.TEACHER: TeacherForm,
        PopupKind.CLASSES: ClassesForm,
        PopupKind.EXPENSES: ExpensesForm,
        PopupKind.INCOME: IncomeForm,
    }

    def _create_content(self, kind: PopupKind, parent=None) -> PopupContentProtocol:
        try:
            form_class = self._content_map[kind]
        except KeyError as error:
            raise ValueError(f"Unsupported popup kind: {kind}") from error

        return form_class(parent=parent)

    def create_window(self, kind: PopupKind, title: str, parent=None) -> BaseWindow:
        content = self._create_content(kind, parent=parent)
        return BaseWindow(title=title, content=content, parent=parent)
    
    
def create_payment_window(self, parent=None):
    return PaymentForm(parent=parent)
