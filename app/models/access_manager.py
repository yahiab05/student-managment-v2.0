

from app.models.admin import Users, Roles


class AccessManager:
    def __init__(self):
        self.user = None
        self.manager = Users()
        self.role_manager = Roles()
        self._access = None
        
    def set_user(self, username):
        self.user = username
        self._access = None  # Reset access when user changes
        
    def set_access(self):
        filters = self.manager.get_filter(username=self.user)
        user = self.manager.get_by_filter(filters)
        if not user:
            return False
        
        filters = self.role_manager.get_filter(role_name=user[0].role_name)
        role = self.role_manager.get_by_filter(filters)
        if not role:
            return False
        
        role = role[0]
        
        self.access = {
            "students": role.students,
            "classes": role.classes,
            "teachers": role.teachers,
            "payment": role.payment,
            "money": role.money,
            "settings": role.settings,
            "user": role.user,
            "payment_edit": role.payment_editting,
        }
        
    def get_access(self, section:str):
        if self.access is None:
            self.set_access()
        
        return self.access.get(section, False)