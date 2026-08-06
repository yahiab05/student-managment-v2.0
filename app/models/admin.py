from .basic_operations import CRUD
from ..utils.utils import error


class Roles(CRUD):
    # Concrete child class for role records that uses the role table.
    def __init__(self, session):
        super().__init__(session, "roles")


class Users(CRUD):
    # Concrete child class for user records that uses the users table.
    def __init__(self, session):
        super().__init__(session, "users")


class Login(CRUD):
    # Concrete child class for login records that uses the login table.
    def __init__(self, session):
        super().__init__(session, "login")
        
    def check_login(self, username, password):
        filters = [
            self.db.table.username == username,
            self.db.table.password == password
        ]
        if not self.exists([filters[0]]):
            error("اسم المستخدم غير صحيح")
            return False
        
        if not self.exists(filters):
            error("كلمة المرور غير صحيحة")
            return False
        
        return True