from abc import ABC, abstractmethod
from report_generator import Printing, ExcelGenerator

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
        
class StrategyFactory:
    def __init__(self, strategy):
        self._strategy = strategy
        
    def export(self):
        self._strategy.export()
        
    @setattr
    def strategy(self, strategy):
        self._strategy = strategy
