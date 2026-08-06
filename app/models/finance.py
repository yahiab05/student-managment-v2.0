from .basic_operations import CRUD


class Income(CRUD):
    # Concrete child class for income records that uses the entery table.
    def __init__(self, session):
        super().__init__(session, "income")
        
    def get_filter(self, code=None):
        filters = []
        if code:
            filters.append(self.db.table.code == code)
        return filters
    
    def check_used(self, code):
        filters = self.get_filter(code)
        return self.exists(filters)


class Expense(CRUD):
    # Concrete child class for expense records that uses the outmoney table.
    def __init__(self, session):
        super().__init__(session, "expenses")
        
    def get_filter(self, code=None, way_payment=None):
        filters = []
        if code:
            filters.append(self.db.table.code == code)
        if way_payment:
            filters.append(self.db.table.way == way_payment)
        return filters
    
    def check_used(self, code):
        filters = self.get_filter(code)
        return self.exists(filters)

