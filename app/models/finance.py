from app.models.names import ModelName
from app.models.basic_operations import CRUD


class Income(CRUD):
    # Concrete child class for income records that uses the entery table.
    def __init__(self, session):
        super().__init__(session, ModelName.INCOME)
        self.set_static_metadata()
        
    def get_filter(self, code=None, name=None, way=None, type=None, addition_from_date=None, 
                addition_to_date=None, price=None, operator=None):
        filters = []
        if code:
            filters.append(self.db.table.code == code)
        if name:
            filters.append(self.db.table.name == name)
        if way:
            filters.append(self.db.table.way == way)
        if type:
            filters.append(self.db.table.type == type)
        if addition_from_date and addition_to_date:
            filters.append(self.db.table.addition_date.between(addition_from_date, addition_to_date))
        if price and operator:
            if operator == "greater":
                filters.append(self.db.table.price > price)
            elif operator == "less":
                filters.append(self.db.table.price < price)
            elif operator == "equal":
                filters.append(self.db.table.price == price)
        return filters
    
    def check_used(self, code):
        filters = self.get_filter(code)
        return self.exists(filters)
    
    def set_static_metadata(self):  

        self.title = "المداخيل"

        self.headers = ["المبلغ", "وسيلة الدخل", "الإسم", "نوع الدخل", "رقم الوصل", "التاريخ"]
        
    def set_dynamic_metadata(self, total_price, data_to_export):
        self.foot = f"""مجموع المداخيل: {total_price}"""
        self.data_to_export = data_to_export
        
class Payment(CRUD):
    def __init__(self, session):
        super().__init__(session, ModelName.INCOME)
        self.set_static_metadata()
        
    def get_filter(self, name=None, way=None, payment_from_date=None, payment_to_date=None, num_inscrit=None, classroom=None):
        filters = []
        if name:
            filters.append(self.db.table.name == name)
        if way:
            filters.append(self.db.table.way == way)
        if payment_from_date and payment_to_date:
            filters.append(self.db.table.payment_date.between(payment_from_date, payment_to_date))
        if num_inscrit:
            filters.append(self.db.table.num_inscrit == num_inscrit)
        if classroom:
            filters.append(self.db.table.classroom == classroom)
        return filters
    
    def set_static_metadata(self):
        self.title = "قائمة الوصولات"

        self.headers = ["طريقة الخلاص", "المبلغ", "مقابل شهر", "بعنوان", "رقم الوصل", "السيد(ة)"]
        
    def set_dynamic_metadata(self, total_price, data_to_export):
        self.foot = f"""مجموع المداخيل: {total_price}"""
        self.data_to_export = data_to_export



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
        super().__init__(session, ModelName.TRANSFER)
        self.set_static_metadata()
        
    def get_filter(self,
            from_date=None,
            to_date=None,
            price=None,
            operator=None,
            ):
        filters = []

        if from_date and to_date:
            filters.append(self.db.table.date.between(from_date, to_date))
        if price and operator:
            if operator == "greater":
                filters.append(self.db.table.price > price)
            elif operator == "less":
                filters.append(self.db.table.price < price)
            elif operator == "equal":
                filters.append(self.db.table.price == price)

        return filters
    
    def set_static_metadata(self):
        self.title = "التحويلات"
        self.headers = ["المبلغ", "الوجهة", "الأصل", "التاريخ"]
        
    def set_dynamic_metadata(self, total_price, data_to_export):
        self.foot = f"""مجموع التحويلات: {total_price}"""
        self.data_to_export = data_to_export
    
class Balance(CRUD):
    # Concrete child class for balance records that uses the balance table.
    def __init__(self, session):
        super().__init__(session)
        self.db = self.repo.get_balance_repo()  # Use the specialized balance repository
        
    def get_balance(self,
            price=None,
            operator=None,
            way=None,
            from_date=None,
            to_date=None):
        income_filters, expense_filters = self.db.get_filters(
            way_payment=way, 
            from_date=from_date, 
            to_date=to_date,
            price=price,
            operator=operator
        )
        return self.db.get_balance(income_filters, expense_filters)

    def get_balance(self, income, expense):
        return income - expense
    
    def set_static_metadata(self):
        self.title = "الحاصل"
        self.headers = ["المبلغ المقبول" ,"المبلغ المصروف", "وسيلة الدخل/المصروف", "التاريخ", "الاسم"]

    def set_dynamic_metadata(self, total_income, total_expenses, balance, data_to_export):
        self.foot = f"""مجموع المداخيل: {total_income} \n 
        مجموع المصاريف: {total_expenses} \n
        الحاصل: {balance}"""
        self.data_to_export = data_to_export