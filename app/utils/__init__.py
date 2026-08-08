from .export_strategy import ReportContext, ReportStrategyFactory
from .combo_manager import ComboManager
from .utils import ( 
    get_username,
    get_student_list,
    error
)
from ..repo.database import SessionLocal

def get_combo_manager():
    session = SessionLocal()
    combo_manager = ComboManager(session)
    return combo_manager

def export_report(report_type, parent, headers, data, title="", intro="", foot=""):
    report = ReportContext()
    strategy = ReportStrategyFactory.get_strategy(report_type, parent)
    report.strategy(strategy)  # Set the strategy
    report.set_data(headers, data, title, intro, foot)
    report.export()

