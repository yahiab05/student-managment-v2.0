from app.view.base_table import BaseTable
from PyQt6.QtCore import Qt

class EnteryTableModel(BaseTable):
    def __init__(self):
        super().__init__()

        self.headers = ["ID", "الاسم", "التاريخ", "المبلغ", "رقم التوصيل", "نوع الدخل", "طريقة الدفع", "ملاحظة", "المستخدم"]

    def data(self, index, role):
        if not index.isValid() or not role == Qt.ItemDataRole.DisplayRole:
            return None
        
        income = self.rows[index.row()]
        column = index.column()
        
        if column == 0:
            return income.id
        elif column == 1:
            return income.name
        elif column == 2:
            return income.addition_date.strftime("%Y-%m-%d")
        elif column == 3:
            return income.price
        elif column == 4:
            return income.bill_number
        elif column == 5:
            return income.type
        elif column == 6:
            return income.way
        elif column == 7:
            return income.note
        elif column == 8:
            return income.user
        return None
    
class OutMoneyTableModel(BaseTable):
    def __init__(self):
        super().__init__()

        self.headers = ["ID", "الاسم", "التاريخ", "المبلغ", "رقم التوصيل", "نوع المصروف", "طريقة الدفع", "ملاحظة", "المستخدم"]

    def data(self, index, role):
        if not index.isValid() or not role == Qt.ItemDataRole.DisplayRole:
            return None
        
        out = self.rows[index.row()]
        column = index.column()
    
        if column == 0:
            return out.id
        elif column == 1:
            return out.name
        elif column == 2:
            return out.date.strftime("%Y-%m-%d")
        elif column == 3:
            return out.price
        elif column == 4:
            return out.bill_num
        elif column == 5:
            return out.type
        elif column == 6:
            return out.way
        elif column == 7:
            return out.note
        elif column == 8:
            return out.user    
        return None
    
class BalanceTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["الاسم", "المصاريف", "المداخيل", "التاريخ", "طريقة الدفع"]

    def data(self, index, role):
        if not index.isValid() or not role == Qt.ItemDataRole.DisplayRole:
            return None   
        
        balances = self.rows[index.row()]
        column = index.column()
    
        if column == 0:
            return balances.name
        elif column == 1:
            return balances.expenses
        elif column == 2:
            return balances.income
        elif column == 3:
            return balances.date.strftime("%Y-%m-%d")
        elif column == 4:
            return balances.way 
        return None           
    
class PaymentTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "رقم الوصل", "الاسم", "رقم التسجيل", "القسم", "مقابل شهر", "أضيف يوم", 
                        "المبلغ","طريقة الدفع", "رقم الصك", "المستخدم"]
                
    def data(self, index, role):
        if not index.isValid() or not role == Qt.ItemDataRole.DisplayRole:
            return None 
        
        payment = self.rows[index.row()]
        column = index.column()
        
        if column == 0:
            return payment.id
        elif column == 1:
            return payment.bill_number
        elif column == 2:
            return payment.name
        elif column == 3:
            return payment.num_inscrit
        elif column == 4:
            return payment.classroom
        elif column == 5:
            return payment.payment_date.strftime("%Y-%m")
        elif column == 6:
            return payment.addition_date.strftime("%Y-%m-%d")
        elif column == 7:
            return payment.price
        elif column == 8:
            return payment.way
        elif column == 9:
            return payment.cheq_num
        elif column == 10:
            return payment.user
        return None
    
class TransferTableModel(BaseTable):
    def __init__(self):
        super().__init__()
        
        self.headers = ["ID", "montant", "origine", "destination", "date", "note", "utilisateur"]        
    def data(self, index, role):
        if not index.isValid() or not role == Qt.ItemDataRole.DisplayRole:
            return None 
        
        transfer = self.rows[index.row()]
        column = index.column()
        
        if column == 0:
            return transfer.id
        elif column == 1:
            return transfer.price
        elif column == 2:
            return transfer.origin
        elif column == 3:
            return transfer.destination
        elif column == 4:
            return transfer.date.strftime("%Y-%m-%d")
        elif column == 5:
            return transfer.note
        elif column == 6:
            return transfer.user
        return None