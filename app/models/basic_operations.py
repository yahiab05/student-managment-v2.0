from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QMessageBox
from ..repo.facade import DBFacade
from ..repo.schemas.base_schema import BaseDataClass
from ..utils import PrintingStrategy, ExcelStrategy, ReportContext


class CRUD(ABC):
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

    def sup_security(self, id):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا الشخص ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete(id)
        else:
            self.reset()

    def delete(self, id):
        try:
            return self.db.delete(id)
        except ModuleNotFoundError:
            raise ValueError("لا يمكن حذف هذا الشخص لأنه مرتبط ببيانات أخرى في النظام.")

    def get_all(self):
        return self.db.get_all()

    def get_by_id(self, id):
        return self.db.get_by_id(id)

    def get_by_filter(self, filters: list):
        # Delegate filter-based queries to the shared database facade.
        return self.db.get_by_filter(filters)
    
    def exists(self, filters: list):
        # Check for existence of records matching the provided filters.
        return self.db.exists(filters)

    def print_preview(self, parent):
        if self.data_to_export is None or self.headers is None:
            raise ValueError("Data and headers must be set before printing.")
        
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
        finally:
            self.data_to_export = None
            
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

    @abstractmethod
    def set_metadata(self):
        pass