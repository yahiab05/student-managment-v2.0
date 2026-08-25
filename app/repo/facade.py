from sqlalchemy import func, union_all
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoSuchColumnError
from app.repo.database import SessionLocal

from contextlib import contextmanager
class DBFacade:
    def __init__(self, table):
        self.table = table
        
    def get_all(self):
        with SessionLocal() as session:
            return session.query(self.table).all()
    
    def get_by_id(self, id, multiple=False):
        with SessionLocal() as session:
            if multiple:
                return session.query(self.table).filter(self.table.id == id).all()
            return session.query(self.table).filter(self.table.id == id).first()
        
    def add(self, data):
        obj = self.table(**data)
        with SessionLocal() as session:
            try:
                session.add(obj)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return obj
    
    def bulk_add(self, data_list):
        data = [self.table(**data) for data in data_list]
        with SessionLocal() as session:
            try:
                session.bulk_save_objects(data)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            
    def get_biggest_id(self):
        with SessionLocal() as session:    
            return session.query(func.max(self.table.id)).scalar()

    def update(self, id, data):
        with SessionLocal() as session:
            try:
                obj = session.query(self.table).filter(self.table.id == id).first()
                if not obj:
                    raise ModuleNotFoundError("Object not found")
                for key, value in data.items():
                    if hasattr(obj, key) and key != "id":
                        setattr(obj, key, value)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return obj
    
    def delete(self, id):
        with SessionLocal() as session:
            try:
                obj = session.query(self.table).filter(self.table.id == id).first()
                if not obj:
                    raise ModuleNotFoundError("Object not found")
                session.delete(obj)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        
    def update_by_filter(self, filters: list, data: dict):
        with SessionLocal() as session:
            try:
                obj = session.query(self.table).filter(*filters).first()
                print(f"Updating object: {obj} with data: {data}")
                if not obj:
                    raise ModuleNotFoundError("Object not found")
                for key, value in data.items():
                    if hasattr(obj, key) and key != "id":
                        setattr(obj, key, value)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return obj
    
    def delete_by_filter(self, filters: list):
        with SessionLocal() as session:
            try:
                obj = session.query(self.table).filter(*filters).first()
                if not obj:
                    raise ModuleNotFoundError("Object not found")
                session.delete(obj)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
                
    def get_by_filter(self, filters:list):
        with SessionLocal() as session:
            data = session.query(self.table).filter(*filters).all()
        return data
    
    def exists(self, filters):
        with SessionLocal() as session:
            return session.query(self.table).filter(*filters).first() is not None
    
    def get_with_joined_load(self, relationship_name: str, filters: list = None):
        """Generic joined-load query.
        
        Eager-loads `relationship_name` on the queried table while applying
        the optional list of filter conditions.
        
        Example:
            repo.get_with_joined_load("student", [StudentsHistory.num_inscrit == 5])
        """
        filters = filters or []
        with SessionLocal() as session:
            return session.query(self.table).options(
                joinedload(getattr(self.table, relationship_name))
            ).filter(*filters).all()

    def get_total(self, filters: list = None) -> float:
        """Calculate the total price of records matching the provided filters."""
        try:
            filters = filters or []
            with SessionLocal() as session:
                total = session.query(self.table).filter(*filters).with_entities(
                    func.sum(self.table.price)
                ).scalar()
            return total or 0
        except NoSuchColumnError as e:
            print(f"Error calculating total: {e}")
            return 0
        
    def update_price(self, id, new_price):
        with SessionLocal() as session: 
            obj = session.query(self.table).filter(self.table.id == id).first()
            try:
                if not obj:
                    raise ModuleNotFoundError("Object not found")
                obj.price = new_price
                session.commit()
                return obj
                
            except AttributeError:
                print(f"Error updating price: Object does not have a 'price' attribute.")
                session.rollback()
                raise            
            except NoSuchColumnError as e:
                print(f"Error updating price: {e}")
                session.rollback()
                raise
            
    @contextmanager
    def transaction(self):
        """Context manager for handling transactions."""
        with SessionLocal() as session:
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Transaction failed: {e}")
                raise

from app.repo.models import Entery, OutMoney
class BalanceFacade():
    """Specialized DBFacade for financial entities with additional methods."""

    def get_filters(self, way_payment=None, from_date=None, to_date=None, price=None, operator=None):
        income_filters = []
        expense_filters = []
        
        if way_payment:
            income_filters.append(Entery.way == way_payment)
            expense_filters.append(OutMoney.way == way_payment)
        if from_date and to_date:
            income_filters.append(Entery.addition_date.between(from_date, to_date))
            expense_filters.append(OutMoney.date.between(from_date, to_date))
        if price and operator:
            if operator == ">":
                income_filters.append(Entery.price > price)
                expense_filters.append(OutMoney.price > price)
            elif operator == "<":
                income_filters.append(Entery.price < price)
                expense_filters.append(OutMoney.price < price)
            elif operator == "=":
                income_filters.append(Entery.price == price)
                expense_filters.append(OutMoney.price == price)
        
        return income_filters, expense_filters
    
    def get_balance(self, income_filters= [], expense_filters= []):
        with SessionLocal() as session:
            income = session.query(
                Entery.name.label("name"),
                Entery.price.label("income"),
                func.coalesce(0, '').label("expenses"),
                Entery.way.label("way"),
            Entery.addition_date.label("date")
        ).filter(*income_filters)

            expenses = session.query(
            OutMoney.name.label("name"),
            func.coalesce(0, '').label("income"),
            OutMoney.price.label("expenses"),
            OutMoney.way.label("way"),
            OutMoney.date.label("date")
        ).filter(*expense_filters)
        
        combined_query = union_all(income, expenses)
        return session.query(combined_query).order_by(combined_query.c.date.desc()).all()