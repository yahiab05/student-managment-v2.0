from abc import ABC
from PyQt6.QtWidgets import QMessageBox, QWidget
from contextlib import contextmanager
from app.repo.schemas.base_schema import BaseDataClass
from app.utils import export_report, ReportType, ReportContext
from app.repo import Repositories


class CRUD(ABC):
    intro: str = None
    data_to_export: list = None
    footer: str = None
    headers: list = None
    title: str = None
    

    def __init__(self, table=None):        
        self.repo = Repositories()
        self.db = self.repo.get_repo(table)
        self.report_context = ReportContext()

    def create(self, data_obj: BaseDataClass, session=None):
        data = data_obj.to_dict()
        return self.db.add(data, _session=session)
    
    def bulk_create(self, data_objs: list[BaseDataClass]):
        data_list = [data_obj.to_dict() for data_obj in data_objs]
        return self.db.bulk_add(data_list)

    def update(self, id, data_obj: BaseDataClass):
        data = data_obj.to_dict()
        try:
            return self.db.update(id, data)
        except ModuleNotFoundError:
            return

    def sup_security(self, widget:QWidget, text, id=0, filter=None):
        msg = QMessageBox()
        ret = msg.question(widget, 'حذف', text, msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            if filter is not None:
                self.delete_by_filter(filter)
            else:
                if id == 0:
                    raise ValueError("ID must be provided for deletion.")
                self.delete(id)
    
    def delete(self, id):
        try:
            return self.db.delete(id)
        except ModuleNotFoundError:
            raise ValueError("لا يمكن حذف هذا الشخص لأنه مرتبط ببيانات أخرى في النظام.")

    def get_all(self):
        return self.db.get_all()

    def get_by_id(self, id, session=None):
        return self.db.get_by_id(id, _session=session)

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
            
    def get_total(self, filters: list = None):
        """Calculate the total price of records matching the provided filters."""
        return self.db.get_total(filters)
    
    def update_price(self, id, new_price):
        """Update the price of a record identified by `id`."""
        try:
            self.db.update_price(id, new_price)
        except ModuleNotFoundError:
            return

    @contextmanager
    def transaction(self):
        """Execute a series of database operations as a single transaction.

        Args:
            operations (list of callables): A list of functions that perform database operations.
        """
        with self.db.transaction() as session:
            yield session