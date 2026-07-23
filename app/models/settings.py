from .basic_operations import CRUD


class Settings(CRUD):
    # Concrete child class for settings records that uses the settings table.
    def __init__(self, session):
        super().__init__(session, "settings")
