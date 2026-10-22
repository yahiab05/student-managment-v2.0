from app.models.names import ModelName
from app.models.basic_operations import CRUD
from app.utils.utils import error


class Roles(CRUD):
    # Concrete child class for role records that uses the role table.
    def __init__(self):
        super().__init__(ModelName.ROLES)
        
    def get_filter(self, role_name=None):
        filters = []
        if role_name:
            filters.append(self.db.table.name == role_name)
        return filters

class Users(CRUD):
    # Concrete child class for user records that uses the users table.
    def __init__(self):
        super().__init__(ModelName.USERS)
        
    def get_filter(self, username=None, role=None):
        filters = []
        if username:
            filters.append(self.db.table.username == username)
        if role:
            filters.append(self.db.table.role == role)
        return filters


class Login(CRUD):
    # Concrete child class for login records that uses the login table.
    def __init__(self):
        super().__init__(table=ModelName.LOGIN)
        
    def check_login(self, username, password):
        filters = [
            self.db.table.username == username,
            self.db.table.password == password
        ]
        if not self.exists([filters[0]]):
            return False, 1  # Username does not exist
        
        if not self.exists(filters):
            return False, 2  # Password is incorrect
        
        return True, 0
