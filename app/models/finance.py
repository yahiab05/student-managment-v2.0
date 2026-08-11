from .names import ModelName
from .basic_operations import CRUD


class Income(CRUD):
    # Concrete child class for income records that uses the entery table.
    def __init__(self, session):
		super().__init__(session, ModelName.INCOME)
        
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
		super().__init__(session, ModelName.EXPENSES)
        self.set_static_metadata()
        
    def get_filters(self, code=None, way_payment=None, name=None,
            type=None,
            from_date=None,
            to_date=None,
            price=None,
            operator=None,
            in_bank=None):
        filters = []
        if code:
            filters.append(self.db.table.code == code)
        if way_payment:
            filters.append(self.db.table.way == way_payment)
        if name:
            filters.append(self.db.table.name == name)
        if type:
            filters.append(self.db.table.type == type)
        if from_date and to_date:
            filters.append(self.db.table.date.between(from_date, to_date))
        if price and operator:
            if operator == "greater":
                filters.append(self.db.table.price > price)
            elif operator == "less":
                filters.append(self.db.table.price < price)
            elif operator == "equal":
                filters.append(self.db.table.price == price)
        if in_bank is not None:
            filters.append(self.db.table.in_bank == in_bank)
        return filters
    
    def check_used(self, code):
        filters = self.get_filters(code)
        return self.exists(filters)
    
    def set_static_metadata(self):
        self.title = "المصاريف"
        self.headers = ["المبلغ", "وسيلة الدفع", "نوع المصروف", "التاريخ", "الرمز"]
        
    def set_dynamic_metadata(self, total_price, data_to_export):
        self.foot = f"""مجموع المصاريف: {total_price}"""
        self.data_to_export = data_to_export

class Transfer(CRUD):
    # Concrete child class for transfer records that uses the transfer table.
    def __init__(self, session):
        super().__init__(session, "transfer")
        
    def get_filter(self):
        pass

