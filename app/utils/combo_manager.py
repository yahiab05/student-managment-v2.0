from ..repo.models import (
    Classes as ClassesCombo,
    Settings as SettingsCombo,
    Teachers as TeachersCombo,
    Role as RolesCombo
    )


class ComboManager:
    def __init__(self, session):
        self.session = session
        self.class_combo = ClassesCombo()
        self.settings_combo = SettingsCombo()
        self.teachers_combo = TeachersCombo()
        self.roles_combo = RolesCombo()
        
        self.cached = {
            "classes": [],
            "way teaching": [],
            "types": [],
            "names": [],
            "income": [],
            "income code": [],
            "expenses": [],
            "expenses code": [],
            "fr": [],
            "way payment": [],
            "teachers": [],
            "roles": []
        }

        self._cache_sources = {
            "classes": (ClassesCombo, "name"),
            "teachers": (TeachersCombo, "name"),
            "roles": (RolesCombo, "name"),
            "way teaching": (SettingsCombo, "way_teaching"),
            "income": (SettingsCombo, "entery"),
            "income code": (SettingsCombo, "entery_code"),
            "expenses": (SettingsCombo, "out_money"),
            "expenses code": (SettingsCombo, "out_code"),
            "fr": (SettingsCombo, "fr"),
            "way payment": (SettingsCombo, "way_payment"),
        }

    def update_cache_from_db(self, data_name):
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

    def get_cached_data(self, data_name):
        """Return the cached content for the requested data name."""
        try:
            return self.cached[data_name]
        except KeyError as error:
            raise KeyError(f"Unknown cached data name: {data_name}") from error
        
    def update_combo(self, combo_widget, data_name):
        """Update a combo box widget with the cached data for the specified name."""
        try:
            data = self.get_cached_data(data_name)
        except KeyError as error:
            raise KeyError(f"Unknown cached data name: {data_name}") from error

        combo_widget.clear()
        combo_widget.addItems(data)
        combo_widget.setCurrentIndex(-1)  # Reset selection to no selection
    
