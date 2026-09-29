
from builtins import KeyError

from PyQt6.QtWidgets import QComboBox
from .combo_names import ComboName, ComboSource

from app.repo.database import SessionLocal


class ComboManager:
    def __init__(self):
        
        self.source = ComboSource()
        
        self._cache_sources = self.source.get_cached_source()
        self.cached = self.source.get_cached_data()

    def update_cache_from_db(self, data_name: ComboName):
        """Refresh one cached list from the database."""
        try:
            model, column_name = self._cache_sources[data_name]
        except KeyError as error:
            raise KeyError(f"Unknown cached data name: {data_name}") from error

        with SessionLocal() as session:
            rows = session.query(model).with_entities(getattr(model, column_name)).all()
        print([row[0] for row in rows])
        self.cached[data_name] = [row[0] for row in rows if row[0] is not None]
        print(f"Updated {data_name} cache with {self.cached[data_name]} entries")
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
        
        self.update_with_data(combo_widget, data)   # Reset selection to no selection
        
    def update_with_data(self, combo_widget: QComboBox, data: list[str]):
        """Update a combo box widget with a specific list of class names."""
        combo_widget.clear()
        combo_widget.addItems(data)
        combo_widget.setCurrentIndex(-1)  # Reset selection to no selection
    
