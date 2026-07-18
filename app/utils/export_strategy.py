from abc import ABC, abstractmethod
from .report_generator import Printing, ExcelGenerator
from PyQt6.QtWidgets import QFileDialog

class Strategy(ABC):
    def __init__(self, headers, data, parent):
        self.headers = headers
        self.data = data
        self.parent = parent
        
    @abstractmethod
    def export(self):
        pass
    
class ExcelStrategy(Strategy):
    def __init__(self, headers, data, parent):
        super().__init__(headers, data, parent)
        
    def export(self):
        file = QFileDialog.getSaveFileName(self.parent, 'Save file', '', '*.xlsx')
        if file[0]:
            ExcelGenerator(self.headers, self.data).excel(file)
        
class PrintingStrategy(Strategy):
    def __init__(self, headers, data, parent, title:str="", intro:str="", foot:str=""):
        super().__init__(headers, data, parent)
        self.title = title
        self.intro = intro
        self.foot = foot
        
    def export(self):
        dialog = Printing()
        dialog.setup_document(self.data, self.headers, self.title, self.intro, self.foot)
        dialog.show()
        
class ReportContext:
    def __init__(self):
        self._strategy = None
        
    def export(self):
        if self._strategy is None:
            raise ValueError("No strategy set")
        self._strategy.export()
        
    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy):
        self._strategy = strategy
