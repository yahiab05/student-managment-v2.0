from .basic_operations import CRUD


class Settings(CRUD):
    # Concrete child class for settings records that uses the settings table.
    def __init__(self, session):
        super().__init__(session, "settings")
        
    def get_filter(self, way_teaching=None, entery=None, out_money=None, way_payment=None, fr=None):
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
        return filters
