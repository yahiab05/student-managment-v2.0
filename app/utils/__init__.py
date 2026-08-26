from app.utils.export_strategy import ReportContext, ReportStrategyFactory
from app.utils.combo_manager import ComboManager, ComboName
from app.utils.utils import ( 
    get_username,
    set_username,
    get_student_list,
    error,
    ReportType,
    WorkingMode, 
    Account, info,
    load_gui, 
    UiPath,
    traceback_to_string
)
from app.repo.database import SessionLocal

def create_combo_manager() -> ComboManager:
    session = SessionLocal()
    combo_manager = ComboManager(session)
    return combo_manager

get_combo_manager = create_combo_manager()  # Create a single instance of ComboManager

def export_report(report_type, parent, headers, data, title="", intro="", foot=""):
    report = ReportContext()
    strategy = ReportStrategyFactory.get_strategy(report_type, parent)
    report.strategy(strategy)  # Set the strategy
    report.set_data(headers, data, title, intro, foot)
    report.export()

