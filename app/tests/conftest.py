import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """A single QApplication instance for the whole test session.

    PyQt6 widgets cannot be instantiated without a running QApplication.
    """
    app = QApplication.instance() or QApplication([])
    yield app
