
class DBFacade:
    def __init__(self, table):
        self.table = table
        
    def get_all(self, session):
        return session.query(self.table).all()  
    
    def add(self, data, session):
        obj = self.table(**data)
        session.add(obj)
        return obj

    def update(self, id, data, session):
        obj = session.query(self.table).where(self.table.id == id).first()
        if not obj:
            raise Exception("Object not found")
        obj.update(**data)
        return obj
    
    def delete(self, id, session):
        obj = session.query(self.table).get(id)
        if not obj:
            raise Exception("Object not found")
        session.delete(obj)
        
    def get_by_filter(self, session, filters:list):
        filters = filters or []
        return session.query(self.table).filter(*filters).all()