from app.repo.models import (
    Classes as ClassesCombo,
    Settings as SettingsCombo,
    Teachers as TeachersCombo,
    Role as RolesCombo
    )
from PyQt6.QtWidgets import QComboBox
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


class ComboManager:
    def __init__(self, session):
        self.session = session
        self.class_combo = ClassesCombo()
        self.settings_combo = SettingsCombo()
        self.teachers_combo = TeachersCombo()
        self.roles_combo = RolesCombo()
        
        self.cached = {
            ComboName.CLASS: [],
            ComboName.WAY_TEACHING: [],
            ComboName.INCOME: [],
            ComboName.EXPENSES: [],
            ComboName.FR: [],
            ComboName.WAY_PAYMENT: [],
            ComboName.TEACHER: [],
            ComboName.ROLE: [],
        }

        self._cache_sources = {
            ComboName.CLASS: (ClassesCombo, "name"),
            ComboName.TEACHER: (TeachersCombo, "name"),
            ComboName.ROLE: (RolesCombo, "name"),
            ComboName.WAY_TEACHING: (SettingsCombo, "way_teaching"),
            ComboName.INCOME: (SettingsCombo, "entery"),
            ComboName.EXPENSES: (SettingsCombo, "out_money"),
            ComboName.FR: (SettingsCombo, "fr"),
            ComboName.WAY_PAYMENT: (SettingsCombo, "way_payment"),
        }

    def update_cache_from_db(self, data_name: ComboName):
        """Refresh one cached list from the database."""
        try:
            model, column_name = self._cache_sources[data_name]
        except KeyError as error:
            raise KeyError(f"Unknown cached data name: {data_name}") from error

        rows = self.session.query(model).with_entities(getattr(model, column_name)).all()
        self.cached[data_name] = [row[0] for row in rows if row[0] is not None]
        return self.cached[data_name]

    def update_all_cache(self):
        """Refresh all supported cache entries from the database."""
        for data_name in self._cache_sources:
            self.update_cache_from_db(data_name)
        return self.cached

    def get_cached_data(self, data_name: ComboName):
        """Return the cached content for the requested data name."""
        try:
            return self.cached[data_name]
        except KeyError as error:
            raise KeyError(f"Unknown cached data name: {data_name}") from error
        
    def update_combo(self, combo_widget: QComboBox, data_name: ComboName):
        """Update a combo box widget with the cached data for the specified name."""
        try:
            data = self.get_cached_data(data_name)
        except KeyError as error:
            raise KeyError(f"Unknown cached data name: {data_name}") from error

        combo_widget.clear()
        combo_widget.addItems(data)
        combo_widget.setCurrentIndex(-1)  # Reset selection to no selection
    
