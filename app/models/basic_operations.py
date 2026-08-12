from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QMessageBox
from app.repo import Repository
from app.repo.schemas.base_schema import BaseDataClass
from app.utils import export_report, ReportType
from app.repo import Repositories


class CRUD(ABC):
    intro: str = None
    data_to_export: list = None
    footer: str = None
    headers: list = None
    title: str = None
    

    def __init__(self, session, table):        
        self.repo = Repositories(session)
        self.db = self.repo.get_repo(table)
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
    
    def update_by_filter(self, filters: list, data_obj: BaseDataClass):
        data = data_obj.to_dict()
        try:
            return self.db.update_by_filter(filters, data)
        except ModuleNotFoundError:
            return
        
    def delete_by_filter(self, filters: list): #this is a comment
        try:
            return self.db.delete_by_filter(filters)
        except ModuleNotFoundError:
            return

    def get_with_joined_load(self, relationship_name: str, filters: list = None):
        """Generic joined-load query helper.

        Eager-loads `relationship_name` on the current table while applying
        optional filter conditions. Returns results with the relationship
        already populated (avoids N+1 queries).

        Example:
            results = self.get_with_joined_load("student", [self.db.table.num_inscrit == 5])
        """
        return self.db.get_with_joined_load(relationship_name, filters)
            
    def export_data(self, report_type: ReportType, parent):
        if self.data_to_export is None or self.headers is None:
            raise ValueError("Data and headers must be set before exporting.")
        
        try:
            export_report(
                report_type=report_type,
                parent=parent,
                headers=self.headers,
                data=self.data_to_export,
                title=self.title,
                intro=self.intro,
                foot=self.footer
            )
        except ValueError as e:
            print(e)
        finally:
            self.data_to_export = None

    @abstractmethod
    def set_metadata(self):
        pass
    
    def rollback(self):
        self.db.rollback()
        
    def commit(self):
        self.db.commit()