from .basic_operations import CRUD


class Settings(CRUD):
    # Concrete child class for settings records that uses the settings table.
    def __init__(self, session):
        super().__init__(session, "settings")
        
    def get_filter(self, way_teaching=None, entery=None, out_money=None, way_payment=None, fr=None,
                    entry_code=None, out_code=None):
        filters = []
        if way_teaching:
            filters.append(self.db.table.way_teaching.ilike(f"%{way_teaching}%"))
        if entery:
            filters.append(self.db.table.entery.ilike(f"%{entery}%"))
        if out_money:
            filters.append(self.db.table.out_money.ilike(f"%{out_money}%"))
        if way_payment:
            filters.append(self.db.table.way_payment.ilike(f"%{way_payment}%"))
        if fr:
            filters.append(self.db.table.fr.ilike(f"%{fr}%"))
        if entry_code:
            filters.append(self.db.table.entry_code == entry_code)
        if out_code:
            filters.append(self.db.table.out_code == out_code)
        return filters
    
    def get_code(self, income, expense):
        filters = []
        if income:
            filters.append(self.db.table.entery == income)
            setting = self.get_by_filter(filters)
            return setting[0].entery_code if setting else None
        elif expense:
            filters.append(self.db.table.out_money == expense)
            setting = self.get_by_filter(filters)
            return setting[0].out_code if setting else None
        
    def get_type(self, income_code=None, expense_code=None):
        filters = []
        if income_code:
            filters.append(self.db.table.entry_code == income_code)
            setting = self.get_by_filter(filters)
            return setting[0].entery if setting else None
        elif expense_code:
            filters.append(self.db.table.out_code == expense_code)
            setting = self.get_by_filter(filters)
            return setting[0].out_money if setting else None