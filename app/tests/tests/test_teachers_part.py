from unittest.mock import MagicMock

import pytest
from PyQt6.QtWidgets import QWidget

from app.controllers import teacher as teacher_pkg_module
from app.controllers.teacher import TeachersPart


class _FakeTeacherLogic(QWidget):
    """Stand-in for the real TeacherLogic sub-controller: a genuine QWidget
    (so QStackedWidget.addWidget accepts it) with a spyable setup_table."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table = MagicMock()


class _FakeTeachersHistoryLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table = MagicMock()


@pytest.fixture
def part(qapp, monkeypatch):
    """A TeachersPart with its two heavy sub-controllers replaced by
    lightweight fakes so we can test the navigation logic in isolation."""
    monkeypatch.setattr(teacher_pkg_module, "TeacherLogic", _FakeTeacherLogic)
    monkeypatch.setattr(teacher_pkg_module, "TeachersHistoryLogic", _FakeTeachersHistoryLogic)
    return TeachersPart()


class TestTeachersPartInit:
    def test_adds_both_subviews_to_stacked_widget(self, part):
        assert part.stackedWidget.count() == 2
        assert part.stackedWidget.widget(0) is part.t
        assert part.stackedWidget.widget(1) is part.th

    def test_starts_on_teachers_tab(self, part):
        assert part.stackedWidget.currentIndex() == 0

    def test_teacher_button_starts_highlighted(self, part):
        assert part.teacher.styleSheet() == "color: green"
        assert part.teacher_history.styleSheet() == "color: white"


class TestNavigation:
    def test_go_to_teachers_switches_to_index_0_and_highlights_button(self, part):
        part.stackedWidget.setCurrentIndex(1)
        part.go_to_teachers()

        assert part.stackedWidget.currentIndex() == 0
        assert part.teacher.styleSheet() == "color: green"
        assert part.teacher_history.styleSheet() == "color: white"

    def test_go_to_history_switches_to_index_1_refreshes_table_and_highlights_button(self, part):
        part.go_to_history()

        assert part.stackedWidget.currentIndex() == 1
        part.th.setup_table.assert_called_once()
        assert part.teacher_history.styleSheet() == "color: green"
        assert part.teacher.styleSheet() == "color: white"

    def test_clicking_teacher_button_navigates_to_teachers_tab(self, part):
        part.stackedWidget.setCurrentIndex(1)
        part.teacher.click()
        assert part.stackedWidget.currentIndex() == 0

    def test_clicking_teacher_history_button_navigates_to_history_tab(self, part):
        part.teacher_history.click()
        assert part.stackedWidget.currentIndex() == 1
        part.th.setup_table.assert_called_once()


class TestButtonsStyling:
    def test_buttons_resets_both_then_highlights_target(self, part):
        part.buttons(part.teacher_history)

        assert part.teacher.styleSheet() == "color: white"
        assert part.teacher_history.styleSheet() == "color: green"
