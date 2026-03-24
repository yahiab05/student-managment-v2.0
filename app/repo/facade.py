from .database import SessionLocal

class DBFacade:
    def __init__(self, table):
        self.table = table
        self.session = SessionLocal
        
    def get_all(self):
        return self.session.query(self.table).all()
    
    def add(self, data):
        obj = self.table(**data)
        self.session.add(obj)
        self.auto_commit(obj)
        return obj
    
    def update(self, id, data):
        obj = self.session.query(self.table).get(id)
        if not obj:
            raise Exception("Object not found")
        obj.update(**data)
        self.auto_commit(obj)
        return obj
    
    def delete(self, id):
        obj = self.session.query(self.table).get(id)
        if not obj:
            raise Exception("Object not found")
        self.session.delete(obj)
        self.auto_commit(obj)
        
    def get_by_filter(self, filters:list=[]):
        return self.session.query(self.table).filter(*filters).all()
    
    def auto_commit(self, obj):
        self.session.commit()
        self.session.refresh(obj)