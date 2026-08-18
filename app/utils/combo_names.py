from app.repo.models import (
    Classes as ClassesCombo,
    Settings as SettingsCombo,
    Teachers as TeachersCombo,
    Role as RolesCombo, 
    ClassEleve as Enrollments
    )
from enum import StrEnum


class ComboName(StrEnum):
    CLASS = "classes"
    TEACHER = "teachers"
    ROLE = "roles"
    WAY_TEACHING = "way teaching"
    INCOME = "income"
    EXPENSES = "expenses"
    FR = "fr"
    WAY_PAYMENT = "way payment"
    ENROLLMENTS = "enrollments"

class ComboSource:
    def __init__(self, session):
        self.session = session
        self.class_combo = ClassesCombo()
        self.settings_combo = SettingsCombo()
        self.teachers_combo = TeachersCombo()
        self.roles_combo = RolesCombo()
        
        self._cache_sources = {
            ComboName.CLASS: (ClassesCombo, "name"),
            ComboName.TEACHER: (TeachersCombo, "name"),
            ComboName.ROLE: (RolesCombo, "name"),
            ComboName.WAY_TEACHING: (SettingsCombo, "way_teaching"),
            ComboName.INCOME: (SettingsCombo, "entery"),
            ComboName.EXPENSES: (SettingsCombo, "out_money"),
            ComboName.FR: (SettingsCombo, "fr"),
            ComboName.WAY_PAYMENT: (SettingsCombo, "way_payment"),
            ComboName.ENROLLMENTS: (Enrollments, "class_name"),
        }
        
        self.cached = {
            ComboName.CLASS: [],
            ComboName.WAY_TEACHING: [],
            ComboName.INCOME: [],
            ComboName.EXPENSES: [],
            ComboName.FR: [],
            ComboName.WAY_PAYMENT: [],
            ComboName.TEACHER: [],
            ComboName.ROLE: [],
            ComboName.ENROLLMENTS: [],
        }
        
    def get_cached_source(self):
        return self._cache_sources
    
    def get_cached_data(self):
        return self.cached