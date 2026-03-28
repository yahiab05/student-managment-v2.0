from .facade import DBFacade 
from .models import *
class Repositories:
    # Core entities
    roles = DBFacade(Role)
    users = DBFacade(Users)
    
    # Student related
    students = DBFacade(Students)
    students_history = DBFacade(StudentsHistory)
    
    # Teacher related
    teachers = DBFacade(Teachers)
    teachers_history = DBFacade(TeachersHistory)
    
    # Class related
    classes = DBFacade(Classes)
    classeleve = DBFacade(ClassEleve)
    
    # Financial entities
    income = DBFacade(Entery)
    expenses = DBFacade(OutMoney)
    caisse = DBFacade(Caisse)
    bank = DBFacade(Bank)
    
    # Settings and other
    settings = DBFacade(Settings)
    
    # Absence tracking
    teachers_absent = DBFacade(AbsentT)
    students_absent = DBFacade(AbsentS)
    