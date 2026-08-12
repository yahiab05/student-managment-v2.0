from typing import Protocol, Optional
from app.utils.report_generator import Printing, ExcelGenerator
from PyQt6.QtWidgets import QFileDialog
from app.utils.utils import ReportType

class Strategy(Protocol):
    headers: str
    data: list
    parent: object
    title: Optional[str]
    intro: Optional[str]
    foot: Optional[str]
    
    def __init__(self, parent):
        ...
    
    def export(self) -> None:
        ...
        
    def set_data(self, headers, data, title:str="", intro:str="", foot:str="") -> None:
        ...
        
class ExcelStrategy:
    def __init__(self, parent):
        self.parent: object = parent      
        self.headers: str = None
        self.data: list = None
        
        self.title: str = None
        self.intro: str = None
        self.foot: str = None
        
    def export(self):
        file = QFileDialog.getSaveFileName(self.parent, 'Save file', '', '*.xlsx')
        if file[0]:
            ExcelGenerator(self.headers, self.data).excel(file)
            
    def set_data(self, headers, data, title:str="", intro:str="", foot:str="") -> None:
        self.headers = headers
        self.data = data
        
class PrintingStrategy(Strategy):
    def __init__(self, parent):
        self.parent: object = parent
        self.data: list = None
        self.headers: str = None
        self.title: str = None
        self.intro: str = None
        self.foot: str = None
        
    def export(self):
        dialog = Printing()
        dialog.setup_document(self.data, self.headers, self.title, self.intro, self.foot)
        dialog.show()
        
    def set_data(self, headers, data, title:str="", intro:str="", foot:str="") -> None:
        self.headers = headers
        self.data = data
        self.title = title
        self.intro = intro
        self.foot = foot
        
class ReportContext:
    def __init__(self):
        self._strategy: Strategy | None = None
        
    def export(self):
        if self._strategy is None:
            raise ValueError("No strategy set")
        self._strategy.export()
        
    def set_data(self, headers, data, title:str="", intro:str="", foot:str="") -> None:
        if self._strategy is None:
            raise ValueError("No strategy set")
        self._strategy.set_data(headers, data, title, intro, foot)
        
    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy):
        self._strategy = strategy
        
class ReportStrategyFactory:
    @staticmethod
    def get_strategy(report_type: ReportType, parent) -> Strategy:
        match report_type:
            case ReportType.PRINT:
                return PrintingStrategy(parent)
            case ReportType.EXCEL:
                return ExcelStrategy(parent)    
            case _:
                raise ValueError(f"Unknown report type: {report_type}")
