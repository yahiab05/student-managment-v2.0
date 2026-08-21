from datetime import date
from unittest.mock import Mock

import app.utils.utils as utils_module
from app.utils.utils import Account, get_student_list, get_username, load_gui, set_username


class FakeSettings:
    store = {}

    def __init__(self, *_args, **_kwargs):
        pass

    def setValue(self, key, value):
        self.store[key] = value

    def value(self, key, default=None):
        return self.store.get(key, default)


def test_username_roundtrip(monkeypatch):
    monkeypatch.setattr(utils_module, "QSettings", FakeSettings)
    FakeSettings.store.clear()

    set_username("tester")

    assert get_username() == "tester"


def test_username_fallback_when_settings_returns_none(monkeypatch):
    class NoneSettings(FakeSettings):
        def value(self, _key, _default=None):
            return None

    monkeypatch.setattr(utils_module, "QSettings", NoneSettings)
    assert get_username() == "yahia"


def test_account_opposite():
    assert Account.BANK.opposite == Account.CAISSE
    assert Account.CAISSE.opposite == Account.BANK


def test_load_gui_validates_inputs():
    try:
        load_gui(ui_file="main.ui", widget=None)
        raise AssertionError("Expected ValueError for missing widget")
    except ValueError as exc:
        assert "Widget must be provided" in str(exc)

    try:
        load_gui(widget=object())
        raise AssertionError("Expected ValueError for missing ui file")
    except ValueError as exc:
        assert "UI file name must be provided" in str(exc)


def test_load_gui_builds_absolute_path(monkeypatch):
    captured = {}

    def fake_load_ui(path_arg, widget_arg):
        captured["path"] = path_arg
        captured["widget"] = widget_arg

    monkeypatch.setattr(utils_module, "loadUi", fake_load_ui)
    widget = object()

    load_gui(prefix="../../ui/", ui_file="main.ui", widget=widget)

    assert captured["path"].endswith("ui/main.ui")
    assert captured["widget"] is widget


def test_get_student_list_returns_matches(db_session, mapped_models):
    students = mapped_models.Students
    db_session.add_all(
        [
            students(
                name="Ali",
                gender="M",
                birthday=date(2010, 1, 1),
                date_inscrit=date(2020, 1, 1),
                parent="P1",
                cin=1,
                activity="active",
                num_tel="111",
                excused="no",
                note="",
                user="u",
            ),
            students(
                name="Omar",
                gender="M",
                birthday=date(2011, 1, 1),
                date_inscrit=date(2021, 1, 1),
                parent="P2",
                cin=2,
                activity="active",
                num_tel="222",
                excused="no",
                note="",
                user="u",
            ),
        ]
    )
    db_session.commit()

    result = get_student_list("al")

    assert len(result) == 1
    assert result[0].name == "Ali"
