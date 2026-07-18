from sqlalchemy.orm import joinedload

class DBFacade:
    def __init__(self, table, session):
        self.table = table
        self.session = session
        
    def get_all(self):
        return self.session.query(self.table).all()  
    
    def add(self, data):
        obj = self.table(**data)
        self.session.add(obj)
        return obj

    def update(self, id, data):
        obj = self.session.query(self.table).filter(self.table.id == id).first()
        if not obj:
            raise ModuleNotFoundError("Object not found")
        for key, value in data.items():
            if hasattr(obj, key) and key != "id":
                setattr(obj, key, value)
        return obj
    
    def delete(self, id):
        obj = self.session.query(self.table).filter(self.table.id == id).first()
        if not obj:
            raise ModuleNotFoundError("Object not found")
        self.session.delete(obj)
        
    def get_by_filter(self, filters:list):
        filters = filters or []
        return self.session.query(self.table).filter(*filters).all()
    
    def exists(self, **filters):
        return self.session.query(self.table).filter_by(**filters).first() is not None
    
    def get_with_joined_load(self, relationship_name, filter_field, filter_value):
        return self.session.query(self.table).options(
            joinedload(getattr(self.table, relationship_name))
        ).filter(filter_field == filter_value).all()