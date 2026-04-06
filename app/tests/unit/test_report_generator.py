# test_report_strategy.py
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Import the module under test (adjust the import name to match your file)
from app.utils.report_generator import (
    ExcelGenerator,
    Printing,
)
from app.utils.export_strategy import (
    ExcelStrategy,
    PrintingStrategy,
    ReportContext
)

# ---------------------------
# Tests for ExcelGenerator
# ---------------------------
class TestExcelGenerator:
    def test_excel_writes_headers_and_data(self):
        """ExcelGenerator should write headers and each row of data."""
        headers = ["Name", "Age"]
        data = [["Alice", 30], ["Bob", 25]]
        mock_workbook = Mock()
        mock_sheet = Mock()

        with patch("report_strategy.xlsxwriter.Workbook", return_value=mock_workbook, create=True) as mock_wb:
            mock_workbook.add_worksheet.return_value = mock_sheet
            generator = ExcelGenerator(headers, data)
            generator.excel(("dummy.xlsx", "xlsx"))

            # Check workbook created with correct file name
            mock_wb.assert_called_once_with("dummy.xlsx")
            mock_workbook.add_worksheet.assert_called_once_with("dataimported")
            # Headers written
            assert mock_sheet.write.call_args_list[0] == ((0, 0, "Name"),)
            assert mock_sheet.write.call_args_list[1] == ((0, 1, "Age"),)
            # Data rows
            assert mock_sheet.write.call_args_list[2] == ((1, 0, "Alice"),)
            assert mock_sheet.write.call_args_list[3] == ((1, 1, 30),)
            assert mock_sheet.write.call_args_list[4] == ((2, 0, "Bob"),)
            assert mock_sheet.write.call_args_list[5] == ((2, 1, 25),)
            mock_workbook.close.assert_called_once()

    def test_excel_handles_file_create_error(self):
        """If xlsxwriter raises FileCreateError, nothing crashes."""
        headers = ["Col1"]
        data = [["val1"]]

        with patch("report_strategy.xlsxwriter.Workbook") as mock_wb:
            mock_wb.side_effect = Exception("xlsxwriter.exceptions.FileCreateError")  # Simulate error
            generator = ExcelGenerator(headers, data)
            # Should not raise
            generator.excel(("readonly.xlsx", "xlsx"))


# ---------------------------
# Tests for ExcelStrategy
# ---------------------------
class TestExcelStrategy:
    def test_export_calls_filedialog_and_generator(self):
        """ExcelStrategy.export should open save dialog and call ExcelGenerator."""
        headers = ["H1"]
        data = [["d1"]]
        parent_mock = Mock()

        with patch("report_strategy.QFileDialog.getSaveFileName") as mock_dialog:
            mock_dialog.return_value = ("/path/to/file.xlsx", "xlsx")
            strategy = ExcelStrategy(headers, data, parent_mock)
            strategy.export()

            mock_dialog.assert_called_once_with(parent_mock, "Save file", "", "*.xlsx")
            # We need to check that ExcelGenerator was instantiated and its excel method called
            # Since ExcelGenerator is imported, we can patch it
            with patch("report_strategy.ExcelGenerator") as mock_gen_class:
                strategy = ExcelStrategy(headers, data, parent_mock)
                strategy.export()
                mock_gen_class.assert_called_once_with(headers, data)
                mock_gen_class.return_value.excel.assert_called_once_with(
                    ("/path/to/file.xlsx", "xlsx")
                )

    def test_export_does_nothing_if_no_file_selected(self):
        """If user cancels the save dialog, nothing should happen."""
        headers = ["H1"]
        data = [["d1"]]
        parent_mock = Mock()

        with patch("report_strategy.QFileDialog.getSaveFileName") as mock_dialog:
            mock_dialog.return_value = ("", "")
            with patch("report_strategy.ExcelGenerator") as mock_gen:
                strategy = ExcelStrategy(headers, data, parent_mock)
                strategy.export()
                mock_gen.assert_not_called()


# ---------------------------
# Tests for PrintingStrategy
# ---------------------------
class TestPrintingStrategy:
    def test_export_creates_printing_dialog_and_sets_up_document(self):
        """PrintingStrategy.export should instantiate Printing, call setup_document and show."""
        headers = ["Col"]
        data = [["val"]]
        parent = Mock()
        title = "Test Title"
        intro = "Intro text"
        foot = "Footer"

        with patch("report_strategy.Printing") as mock_printing_class:
            mock_dialog = Mock()
            mock_printing_class.return_value = mock_dialog

            strategy = PrintingStrategy(headers, data, parent, title, intro, foot)
            strategy.export()

            mock_printing_class.assert_called_once()
            mock_dialog.setup_document.assert_called_once_with(
                data, headers, title, intro, foot
            )
            mock_dialog.show.assert_called_once()


# ---------------------------
# Tests for ReportContext
# ---------------------------
class TestReportContext:
    def test_export_delegates_to_strategy(self):
        strategy_mock = Mock()
        context = ReportContext(strategy_mock)
        context.export()
        strategy_mock.export.assert_called_once()

    def test_strategy_property_getter_and_setter(self):
        strategy1 = Mock()
        strategy2 = Mock()
        context = ReportContext(strategy1)
        assert context.strategy is strategy1
        context.strategy = strategy2
        assert context.strategy is strategy2
        context.export()
        strategy2.export.assert_called_once()
        strategy1.export.assert_not_called()


# ---------------------------
# Tests for Printing (QDialog)
# ---------------------------
class TestPrinting:
    @pytest.fixture(autouse=True)
    def mock_qt_dependencies(self):
        """Mock all Qt classes that would otherwise require a QApplication."""
        with patch.multiple(
            "report_strategy",
            QDialog=Mock,
            QApplication=Mock,
            QPrinter=Mock,
            QPrintDialog=Mock,
            loadUi=Mock,
            QPlainTextEdit=Mock,      # printing_plain is a QPlainTextEdit
            Qt=Mock,                  # for Qt.AlignmentFlag
            Template=Mock,            # from jinja2 or string.Template? The code uses Template from ??? Actually it uses Template(string) but no import. We'll patch.
        ):
            # The original code uses `from string import Template`? It doesn't show import,
            # but it uses `Template(table).render(...)`. We'll mock it as a simple callable.
            with patch("report_strategy.Template") as mock_template:
                mock_template_instance = Mock()
                mock_template.return_value = mock_template_instance
                mock_template_instance.render.return_value = "<table>mocked</table>"
                yield

    def test_setup_document_appends_html(self, monkeypatch):
        """setup_document should clear the text edit, set fonts, and append generated HTML."""
        # Create a minimal mock for the dialog's attributes
        printing = Printing()
        printing.printing_plain = Mock()
        printing.printing_plain.clear = Mock()
        printing.printing_plain.setFontPointSize = Mock()
        printing.printing_plain.setAlignment = Mock()
        printing.printing_plain.append = Mock()

        headers = ["H1", "H2"]
        data = [["a", "b"], ["c", "d"]]
        title = "My Title"
        intro = "Intro"
        foot = "Foot"

        printing.setup_document(data, headers, title, intro, foot)

        # Verify the template was rendered with correct context
        from report_strategy import Template
        Template.assert_called_once()
        # The table template string is long; we can check the render call
        mock_template_instance = Template.return_value
        mock_template_instance.render.assert_called_once_with(
            headers=headers, rows=data
        )

        # Check sequence of operations on printing_plain
        printing.printing_plain.clear.assert_called_once()
        # There are multiple setFontPointSize calls: first 20, then 12, then 12 again
        assert printing.printing_plain.setFontPointSize.call_count >= 3
        printing.printing_plain.append.assert_any_call(title)
        printing.printing_plain.append.assert_any_call(intro)
        printing.printing_plain.append.assert_any_call("<table>mocked</table>")
        printing.printing_plain.append.assert_any_call(foot)

    def test_print_file_shows_print_dialog_and_prints(self, monkeypatch):
        """print_file should open QPrintDialog and if accepted call print on the plain text edit."""
        printing = Printing()
        printing.printing_plain = Mock()
        printing.canceled = Mock()

        mock_printer = Mock()
        mock_dialog = Mock()
        mock_dialog.exec.return_value = Mock()  # We'll set the return value to simulate accepted

        with patch("report_strategy.QPrinter") as mock_qprinter, \
            patch("report_strategy.QPrintDialog") as mock_qprintdialog:
            mock_qprinter.return_value = mock_printer
            mock_qprintdialog.return_value = mock_dialog

            # Simulate user accepting the print dialog
            mock_dialog.exec.return_value = Mock(DialogCode=Mock(Accepted=1))
            # Need to simulate the DialogCode.Accepted comparison.
            # In real code: if dialog.exec() == QPrintDialog.DialogCode.Accepted
            # We'll patch QPrintDialog.DialogCode.Accepted to be a value that matches
            mock_dialog.exec.return_value = 1
            with patch("report_strategy.QPrintDialog.DialogCode") as mock_code:
                mock_code.Accepted = 1
                printing.print_file()

            mock_qprinter.assert_called_once()  # default HighResolution
            mock_qprintdialog.assert_called_once_with(mock_printer, printing)
            mock_dialog.exec.assert_called_once()
            printing.printing_plain.print.assert_called_once_with(mock_printer)
            printing.canceled.assert_called_once()

    def test_print_file_does_nothing_if_dialog_cancelled(self, monkeypatch):
        """If user cancels print dialog, no printing occurs."""
        printing = Printing()
        printing.printing_plain = Mock()
        printing.canceled = Mock()

        with patch("report_strategy.QPrinter"), patch("report_strategy.QPrintDialog") as mock_qprintdialog:
            mock_dialog = Mock()
            mock_dialog.exec.return_value = 0  # Not Accepted
            mock_qprintdialog.return_value = mock_dialog
            with patch("report_strategy.QPrintDialog.DialogCode") as mock_code:
                mock_code.Accepted = 1
                printing.print_file()

            printing.printing_plain.print.assert_not_called()
            printing.canceled.assert_not_called()

    def test_canceled_closes_dialog(self):
        """canceled method should call close."""
        printing = Printing()
        printing.close = Mock()
        printing.canceled()
        printing.close.assert_called_once()

    def test_adapt_size_sets_min_and_max_height(self, monkeypatch):
        """adapt_size should query screen height and set dialog height limits."""
        # Mock QApplication.primaryScreen().geometry().height()
        mock_screen = Mock()
        mock_screen.height.return_value = 1000
        with patch("report_strategy.QApplication.primaryScreen", return_value=mock_screen):
            printing = Printing()
            printing.setMinimumHeight = Mock()
            printing.setMaximumHeight = Mock()
            printing.adapt_size()
            printing.setMinimumHeight.assert_called_once_with(int(1000 * 0.6))  # 600
            printing.setMaximumHeight.assert_called_once_with(int(1000 * 0.9))  # 900