from ..repo.models import Role as RoleModel, Users as UsersModel
from .basic_operations import CRUD


class Roles(CRUD):
    # Concrete child class for role records that uses the role table.
    def __init__(self, session):
        super().__init__(session, RoleModel)


class Users(CRUD):
    # Concrete child class for user records that uses the users table.
    def __init__(self, session):
        super().__init__(session, UsersModel)
