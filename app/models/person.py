from abc import ABC
from ..repo.facade import DBFacade
from ..repo.models import Students, Teachers
from ..repo.schemas.base_schema import BaseDataClass
from ..utils import PrintingStrategy, ExcelStrategy, ReportContext


class Person(ABC):
    intro: str = None
    data_to_export: list = None
    footer: str = None
    headers: list = None
    title: str = None

    def __init__(self, session, table):
        self.db = DBFacade(table, session)
        self.report_context = ReportContext()

    def create(self, data_obj: BaseDataClass):
        data = data_obj.to_dict()
        return self.db.add(data)

    def update(self, id, data_obj: BaseDataClass):
        data = data_obj.to_dict()
        try:
            return self.db.update(id, data)
        except ModuleNotFoundError:
            return

    def delete(self, id):
        try:
            return self.db.delete(id)
        except ModuleNotFoundError:
            return

    def get_all(self):
        return self.db.get_all()

    def get_by_id(self, id):
        return self.db.get_by_id(id)

    def get_by_filter(self, filters: list):
        # Delegate filter-based queries to the shared database facade.
        return self.db.get_by_filter(filters)

    def print_preview(self, parent):
        strategy = PrintingStrategy(
            headers=self.headers,
            data=self.data_to_export,
            parent=parent,
            title=self.title,
            intro=self.intro,
            foot=self.footer
        )
        self.report_context.strategy = strategy
        try:
            self.report_context.export()
        except ValueError as e:
            print(e)

    def export_to_excel(self, parent):
        strategy = ExcelStrategy(
            headers=self.headers,
            data=self.data_to_export,
            parent=parent
        )
        self.report_context.strategy = strategy
        try:
            self.report_context.export()
        except ValueError as e:
            print(e)


class Student(Person):
    # Concrete child class for student records that uses the students table.
    def __init__(self, session):
        super().__init__(session, Students)


class Teacher(Person):
    # Concrete child class for teacher records that uses the teachers table.
    def __init__(self, session):
        super().__init__(session, Teachers)

