from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.controllers.teacher import teachers as teachers_module
from app.controllers.teacher.teachers import TeacherLogic, TeachersHistoryLogic
from app.utils import ReportType, WorkingMode


def _integrity_error():
    return IntegrityError("stmt", {}, Exception("boom"))


@pytest.fixture
def teacher_logic(qapp, monkeypatch):
    monkeypatch.setattr(teachers_module, "error", MagicMock())
    logic = TeacherLogic()
    # Replace the collaborators created inside __init__ with plain mocks so
    # each test only exercises TeacherLogic's own logic.
    logic.manager = MagicMock()
    logic.combo_manager = MagicMock()
    logic.classes_manager = MagicMock()
    logic.history_manager = MagicMock()
    return logic


@pytest.fixture
def history_logic(qapp, monkeypatch):
    monkeypatch.setattr(teachers_module, "error", MagicMock())
    logic = TeachersHistoryLogic()
    logic.manager = MagicMock()
    return logic


class TestTeacherLogicInit:
    def test_wires_up_buttons(self, teacher_logic):
        assert teacher_logic.add_btn.receivers(teacher_logic.add_btn.clicked) >= 1
        assert teacher_logic.update_btn.receivers(teacher_logic.update_btn.clicked) >= 1
        assert teacher_logic.delete_btn.receivers(teacher_logic.delete_btn.clicked) >= 1

    def test_loads_teachers_on_init(self, qapp, monkeypatch):
        monkeypatch.setattr(teachers_module, "error", MagicMock())
        logic = TeacherLogic()
        # show_teachers() ran during __init__ and populated the count label
        # from the (empty) fake table model.
        assert logic.nb.text() == "0"

    def test_identifier_starts_as_none(self, teacher_logic):
        assert teacher_logic.identifier is None


class TestShowTeachers:
    def test_uses_search_text_as_filter_when_present(self, teacher_logic):
        teacher_logic.search.setText("Ali")
        teacher_logic.manager.get_filters.return_value = "FILTERS"
        teacher_logic.manager.get_by_filter.return_value = [{"id": 1}]

        teacher_logic.show_teachers()

        teacher_logic.manager.get_filters.assert_called_with("Ali")
        teacher_logic.manager.get_by_filter.assert_called_with("FILTERS")
        assert teacher_logic.nb.text() == "1"

    def test_empty_search_text_becomes_none(self, teacher_logic):
        teacher_logic.search.setText("")
        teacher_logic.manager.get_by_filter.return_value = []

        teacher_logic.show_teachers()

        teacher_logic.manager.get_filters.assert_called_with(None)


class TestSelectRow:
    def test_no_selection_shows_error(self, teacher_logic, monkeypatch):
        teacher_logic.teachers_table.selectionModel = MagicMock(
            return_value=MagicMock(selectedRows=MagicMock(return_value=[]))
        )
        teacher_logic.select_row()
        teachers_module.error.assert_called_once_with("يرجى تحديد قسم")

    def test_selection_sets_identifier_from_model(self, teacher_logic):
        row_index_holder = MagicMock()
        row_index_holder.row.return_value = 2
        teacher_logic.teachers_table.selectionModel = MagicMock(
            return_value=MagicMock(selectedRows=MagicMock(return_value=[row_index_holder]))
        )
        teacher_logic.model = MagicMock()
        teacher_logic.model.index.return_value = "INDEX"
        teacher_logic.model.data.return_value = 42

        teacher_logic.select_row()

        teacher_logic.model.index.assert_called_once_with(2, 0)
        teacher_logic.model.data.assert_called_once_with("INDEX", role=0)
        assert teacher_logic.identifier == 42


class TestControl:
    def _base_data(self, **overrides):
        data = {
            "name": "Ali",
            "date_inscrit": "2024-01-01",
            "birthday": "1990-01-01",
            "phone": "12345678",
            "phone_2": "",
            "note": "",
        }
        data.update(overrides)
        return data

    def test_merges_second_phone_when_valid(self, teacher_logic, monkeypatch):
        captured = {}

        def fake_teacher(**kwargs):
            captured.update(kwargs)
            entity = MagicMock()
            entity.validate.return_value = True
            return entity

        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(fake_teacher)
        )
        # add_history is called by control() with a `date_inscrit=` keyword
        # that doesn't match add_history's real `date` positional param -
        # a pre-existing bug in the source, unrelated to what this test
        # covers (phone merging), so it's stubbed out here.
        teacher_logic.add_history = MagicMock()
        data = self._base_data(phone="11111111", phone_2="22222222")

        teacher_logic.control(WorkingMode.ADD, data)

        assert captured["phone"] == "11111111/22222222"

    def test_invalid_second_phone_is_ignored(self, teacher_logic, monkeypatch):
        captured = {}

        def fake_teacher(**kwargs):
            captured.update(kwargs)
            entity = MagicMock()
            entity.validate.return_value = True
            return entity

        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(fake_teacher)
        )
        teacher_logic.add_history = MagicMock()  # see note above
        data = self._base_data(phone="11111111", phone_2="not-digits")

        teacher_logic.control(WorkingMode.ADD, data)

        assert captured["phone"] == "11111111"

    def test_validation_failure_shows_error_and_stops(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = False
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(lambda **kw: entity)
        )

        teacher_logic.control(WorkingMode.ADD, self._base_data())

        teachers_module.error.assert_called_once_with("الرجاء ملء جميع الحقول")
        teacher_logic.manager.create.assert_not_called()

    def test_validation_raising_value_error_shows_message(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.side_effect = ValueError("bad phone")
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(lambda **kw: entity)
        )

        teacher_logic.control(WorkingMode.ADD, self._base_data())

        teachers_module.error.assert_called_once_with("bad phone")
        teacher_logic.manager.create.assert_not_called()

    def test_add_creates_teacher_and_history_then_refreshes(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = True
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(lambda **kw: entity)
        )
        teacher_logic.manager.get_last_id.return_value = 7
        teacher_logic.add_history = MagicMock()
        teacher_logic.show_teachers = MagicMock()

        data = self._base_data()
        teacher_logic.control(WorkingMode.ADD, data)

        teacher_logic.manager.create.assert_called_once_with(entity)
        teacher_logic.add_history.assert_called_once_with(7, date_inscrit=data["date_inscrit"])
        teacher_logic.show_teachers.assert_called_once()
        teacher_logic.combo_manager.update_cache_from_db.assert_called_once_with("teachers")

    def test_add_duplicate_teacher_shows_error(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = True
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(lambda **kw: entity)
        )
        teacher_logic.manager.create.side_effect = _integrity_error()
        teacher_logic.show_teachers = MagicMock()

        teacher_logic.control(WorkingMode.ADD, self._base_data())

        teachers_module.error.assert_called_once_with("هذا المعلم موجود.")
        teacher_logic.show_teachers.assert_not_called()

    def test_update_without_identifier_shows_error(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = True
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(lambda **kw: entity)
        )
        teacher_logic.identifier = None
        teacher_logic.show_teachers = MagicMock()

        teacher_logic.control(WorkingMode.UPDATE, self._base_data())

        teachers_module.error.assert_called_once_with("يرجى تحديد معلم")
        teacher_logic.manager.update.assert_not_called()

    def test_update_success_resets_identifier_and_refreshes(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = True
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(lambda **kw: entity)
        )
        teacher_logic.identifier = 5
        teacher_logic.show_teachers = MagicMock()

        teacher_logic.control(WorkingMode.UPDATE, self._base_data())

        teacher_logic.manager.update.assert_called_once_with(5, entity)
        assert teacher_logic.identifier is None
        teacher_logic.show_teachers.assert_called_once()

    def test_update_integrity_error_shows_error(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = True
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER", staticmethod(lambda **kw: entity)
        )
        teacher_logic.identifier = 5
        teacher_logic.manager.update.side_effect = _integrity_error()
        teacher_logic.show_teachers = MagicMock()

        teacher_logic.control(WorkingMode.UPDATE, self._base_data())

        teachers_module.error.assert_called_once_with("حدث خطأ أثناء تحديث المعلم.")
        teacher_logic.show_teachers.assert_not_called()


class TestNewYear:
    def test_updates_date_and_commits(self, teacher_logic):
        teacher = MagicMock()
        teacher_logic.manager.get_by_id.return_value = teacher
        teacher_logic.show_teachers = MagicMock()

        teacher_logic.new_year(3)

        teacher_logic.manager.get_by_id.assert_called_once_with(3)
        teacher_logic.manager.commit.assert_called_once()
        teacher_logic.show_teachers.assert_called_once()

    def test_missing_teacher_shows_error(self, teacher_logic):
        teacher_logic.manager.get_by_id.return_value = None
        teacher_logic.new_year(999)
        teachers_module.error.assert_called_once_with("هذا المعلم غير موجود.")

    def test_integrity_error_on_commit_shows_error(self, teacher_logic):
        teacher = MagicMock()
        teacher_logic.manager.get_by_id.return_value = teacher
        teacher_logic.manager.commit.side_effect = _integrity_error()
        teacher_logic.show_teachers = MagicMock()

        teacher_logic.new_year(3)

        teachers_module.error.assert_called_once_with("هذا المعلم موجود.")
        teacher_logic.show_teachers.assert_called_once()


class TestAddHistory:
    def test_creates_history_entry_on_success(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = True
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER_HISTORY", staticmethod(lambda **kw: entity)
        )
        fake_date = MagicMock()
        fake_date.toPyDate.return_value = "2024-01-01"

        teacher_logic.add_history(1, fake_date)

        teacher_logic.history_manager.create.assert_called_once_with(entity)

    def test_validation_failure_prevents_create(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = False
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER_HISTORY", staticmethod(lambda **kw: entity)
        )
        fake_date = MagicMock()

        teacher_logic.add_history(1, fake_date)

        teacher_logic.history_manager.create.assert_not_called()
        teachers_module.error.assert_called_once_with("الرجاء ملء جميع الحقول")

    def test_integrity_error_shows_message(self, teacher_logic, monkeypatch):
        entity = MagicMock()
        entity.validate.return_value = True
        monkeypatch.setattr(
            teachers_module.SchemaFactory, "TEACHER_HISTORY", staticmethod(lambda **kw: entity)
        )
        teacher_logic.history_manager.create.side_effect = _integrity_error()
        fake_date = MagicMock()

        teacher_logic.add_history(1, fake_date)

        teachers_module.error.assert_called_once_with("لم تتم الاضافة")


class TestExport:
    def test_export_delegates_to_manager(self, teacher_logic):
        teacher_logic.model = MagicMock()
        teacher_logic.model.get_current_data.return_value = ["row"]
        teacher_logic.model.rowCount.return_value = 1

        teacher_logic.export(ReportType.EXCEL)

        teacher_logic.manager.set_dynamic_metadata.assert_called_once_with(["row"], 1)
        teacher_logic.manager.export_data.assert_called_once_with(
            report_type=ReportType.EXCEL, parent=teacher_logic
        )


class TestTeachersHistoryLogic:
    def test_show_table_treats_empty_string_as_none(self, history_logic):
        history_logic.manager.search_by_id.return_value = []
        history_logic.show_table("")
        history_logic.manager.search_by_id.assert_called_once_with(None)

    def test_show_table_passes_through_teacher_id_and_updates_count(self, history_logic):
        history_logic.manager.search_by_id.return_value = [1, 2, 3]
        history_logic.show_table(7)
        history_logic.manager.search_by_id.assert_called_once_with(7)
        assert history_logic.nb.text() == "3"

    def test_export_delegates_to_manager(self, history_logic):
        history_logic.model = MagicMock()
        history_logic.model.get_current_data.return_value = ["row"]
        history_logic.model.rowCount.return_value = 1

        history_logic.export(ReportType.PRINT)

        history_logic.manager.set_dynamic_metadata.assert_called_once_with(["row"], 1)
        history_logic.manager.export_data.assert_called_once_with(
            report_type=ReportType.PRINT, parent=history_logic
        )
