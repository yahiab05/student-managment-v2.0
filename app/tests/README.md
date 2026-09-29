# Unit tests for controller_factory.py, __init__.py (x2), login.py, mainWindow.py, teachers.py

## Status
73 tests, all passing, order-independent (verified with pytest-randomly).

## What's in here

```
app/                    <- YOUR 6 REAL FILES + minimal stand-in modules
  controllers/
    __init__.py          REAL FILE (main())
    controller_factory.py REAL FILE
    login.py              REAL FILE
    mainWindow.py         REAL FILE
    teacher/
      __init__.py         REAL FILE (TeachersPart)
      teachers.py         REAL FILE
    classes.py, students.py, payment.py, others.py, popup.py   <- STUBS
  models.py, utils.py, view.py, repo/, ui/                     <- STUBS
tests/                  <- the actual test suite
conftest.py             <- shared QApplication (offscreen) fixture
pytest.ini
requirements-test.txt
```

**Why the stubs exist:** your 6 files import from `app.models`, `app.utils`,
`app.ui.ui_forms`, `app.view`, `app.repo`, and sibling controllers
(`app.controllers.classes/students/payment/others/popup`) that weren't part
of the upload. Since those don't exist, the real files can't even be
imported, let alone tested. The stub modules exist purely to make the
package importable — most stub functions are no-ops or return
`unittest.mock.MagicMock()`, and tests override them further as needed.
The one stub with real logic is `app/utils.py::load_gui`, which attaches
the widget attributes (buttons, line edits, etc.) that each real `.ui`
file is known to define, since the code reads things like `self.submit`
or `self.teachers_table` directly.

## Using this against your real project

Delete the `app/` folder here and drop `tests/`, `conftest.py`, and
`pytest.ini` into your actual project root (next to your real `app/`
package). Most tests should keep working unchanged since they patch
functions by name (`monkeypatch.setattr(module, "get_model", ...)`) rather
than depending on stub internals. You may need to adjust:

- `load_gui` patches, if your real `.ui` files expose different widget
  names than assumed here (see `_UI_ATTRIBUTES` map I inferred from the
  code's `self.<widget>` usages).
- `SchemaFactory.TEACHER` / `TEACHER_HISTORY` validation stubs, since your
  real schema classes may validate differently.
- `FakeTableModel` in `app/view.py`, if your real table model's `.data()`
  format differs.

## Running

```bash
pip install -r requirements-test.txt
QT_QPA_PLATFORM=offscreen pytest -q
```
(`QT_QPA_PLATFORM=offscreen` avoids needing a real display; PyQt6 needs a
`QApplication` to construct any widget.)

## A real bug the tests found

In `teachers.py`, `TeacherLogic.control()` calls:
```python
self.add_history(self.manager.get_last_id(), date_inscrit=data["date_inscrit"])
```
but `add_history(self, teacher_id, date)` takes a positional `date`, not a
`date_inscrit` keyword. As written, every successful "add teacher" raises
`TypeError`. Tests that exercise `control()` for other purposes stub out
`add_history` to isolate what they're actually testing; there's no test
asserting the buggy call succeeds, since it can't.

Also worth checking: `has_classes(self, name)` requires a `name` argument,
but `delete()` calls `self.has_classes()` with none — same class of bug,
not covered by these tests since it wasn't the focus, but worth a look.

## Test breakdown

| File | Covers |
|---|---|
| `test_controller_factory.py` | `ControllerSection` enum, `ControllerFactory` mapping/create/setup/switch |
| `test_login.py` | `Login.__init__`, `setup`, `check_login`, `open_app`, `set_access` |
| `test_main_window.py` | `mainWindow.__init__` wiring, `closeEvent`, `backup_mysql_db` (success/failure/missing dir/missing env vars), `access_control` |
| `test_teachers_part.py` | `TeachersPart` tab navigation and button styling |
| `test_teachers_logic.py` | `TeacherLogic` (show/select/control/new_year/add_history/export) and `TeachersHistoryLogic` |
| `test_app_entrypoint.py` | `main()` |
