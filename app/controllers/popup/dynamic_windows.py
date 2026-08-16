from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget
from PyQt6.QtCore import QDate
from typing import Protocol

from app.repo.schemas import SchemaFactory, EntrySchema
from app.utils import get_combo_manager, ComboName, get_student_list, get_username, error, info, load_gui, UiPath
from app.view import create_table_model, TableType
from app.models import get_model, ModelName

from app.ui.ui_forms import (
    ClassesFormUI,
    ExpensesFormUI,
    IncomeFormUI,
    StudentFormUI,
    TeacherFormUI,
    AddPaymentUI
)

class FormProtocol(Protocol):
    def __init__(self, parent=None): ...

    def get_data(self) -> dict: ...
        
    def repopulate_fields(self, data: dict) -> None: ...

class FormWithCombosToPopulateProtocol(FormProtocol, Protocol):
    def populate_combos(self) -> None: ...

class StudentForm(QWidget, StudentFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_gui(UiPath.FORMS, "student_form.ui", self)
        
    def get_data(self):
        return {
            "name": self.name.text(),
            "parent": self.parent_ent.text(),
            "num_tel": self.num_tel.text(),
            "num_tel_2": self.num_tel_2.text(),
            "cin": self.cin.text(),
            "birthday": self.birthday.date().toPyDate(),
            "activity": self.activity.currentText(),
            "excused": self.excused.currentText(),
            "date_inscrit": self.date_inscrit.date().toPyDate(),
            "note":self.note.text(),
            "gender": self.gender.currentText()
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.parent_ent.setText(data.get("parent", ""))
        self.num_tel.setText(data.get("num_tel", ""))
        self.num_tel_2.setText(data.get("num_tel_2", ""))
        self.cin.setText(data.get("cin", ""))
        self.birthday.setDate(data.get("birthday", self.birthday.date()))
        self.activity.setCurrentText(data.get("activity", ""))
        self.excused.setCurrentText(data.get("excused", ""))
        self.date_inscrit.setDate(data.get("date_inscrit", self.date_inscrit.date()))
        self.note.setText(data.get("note", ""))
        self.gender.setCurrentText(data.get("gender", ""))


class TeacherForm(QWidget, TeacherFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_gui(UiPath.FORMS, "teacher_form.ui", self)

    def get_data(self):
        return {
            "name": self.name.text(),
            "date_inscrit": self.date_inscrit.date().toPyDate(),
            "birthday": self.birthday.date().toPyDate(),
            "phone": self.phone.text(),
            "phone_2": self.phone_2.text(),
            "note": self.note.text(),
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.date_inscrit.setDate(data.get("date_inscrit", self.date_inscrit.date()))
        self.birthday.setDate(data.get("birthday", self.birthday.date()))
        self.phone.setText(data.get("phone", ""))
        self.phone_2.setText(data.get("phone_2", ""))
        self.note.setText(data.get("note", ""))


class ClassesForm(QWidget, ClassesFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_gui(UiPath.FORMS, "classes_form.ui", self)

        self.combo_manager = get_combo_manager()

    def get_data(self):
        return {
            "name": self.name.text(),
            "way": self.way.currentText(),
            "price": self.price.text(),
            "note": self.note.text(),
            "teacher": self.teacher.currentText(),
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.way.setCurrentText(data.get("way", ""))
        self.price.setText(data.get("price", ""))
        self.note.setText(data.get("note", ""))
        self.teacher.setCurrentText(data.get("teacher", ""))
        
    def populate_combos(self) -> None:
        self.combo_manager.update_combo(self.teacher, ComboName.TEACHER)
        self.combo_manager.update_combo(self.way, ComboName.WAY_TEACHING)


class ExpensesForm(QWidget, ExpensesFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_gui(UiPath.FORMS, "expenses_form.ui", self)

        self.combo_manager = get_combo_manager()
        self.settings_manager = get_model(ModelName.SETTINGS)
        
        self.setup_connections()
        
    def setup_connections(self):
        self.way.currentTextChanged.connect(self.cheq_num_on_off)
        self.type.currentTextChanged.connect(self.get_code)
        self.code_input.valueChanged.connect(self.get_type)

    def get_data(self):
        return {
            "name": self.name.currentText(),
            "bill_num": self.bill_num.text(),
            "way": self.way.currentText(),
            "code_input": self.code_input.value(),
            "date": self.date.date().toPyDate(),
            "type": self.type.currentText(),
            "bank_caisse": self.bank_caisse.currentText(),
            "note": self.note.text(),
            "nb_cheque": self.nb_cheque.text(),
            "price": self.price.value(),
        }

    def repopulate_fields(self, data: dict) -> None:
        self.name.setCurrentText(data.get("name", ""))
        self.bill_num.setText(data.get("bill_num", ""))
        self.way.setCurrentText(data.get("way", ""))
        self.code_input.setValue(data.get("code_input", 0))
        self.date.setDate(data.get("date", self.date.date()))
        self.type.setCurrentText(data.get("type", ""))
        self.bank_caisse.setCurrentText(data.get("bank_caisse", ""))
        self.note.setText(data.get("note", ""))
        self.nb_cheque.setText(data.get("nb_cheque", ""))
        self.price.setValue(data.get("price", 0.0))
        
    def populate_combos(self) -> None:
        self.combo_manager.update_combo(self.name, ComboName.FR)
        self.combo_manager.update_combo(self.way, ComboName.WAY_PAYMENT)
        self.combo_manager.update_combo(self.type, ComboName.EXPENSES)  
        
    def cheq_num_on_off(self):
        if self.way.currentText() == "صك":
            self.nb_cheque.setEnabled(True)
        else:    
            self.nb_cheque.setEnabled(False)
            
    def get_code(self):
        code = self.settings_manager.get_code(
            income=None, 
            expense=self.type.currentText()
            )
        self.code_input.setValue(code if code is not None else 0)

    def get_type(self):
        expense = self.settings_manager.get_type(
            income_code=None,
            expense_code=self.code_input.value()
            )
        self.type.setCurrentText(expense if expense is not None else "")

class IncomeForm(QWidget, IncomeFormUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_gui(UiPath.FORMS, "income_from.ui", self)

        self.combo_manager = get_combo_manager()
        self.settings_manager = get_model(ModelName.SETTINGS)
        
    def setup_connections(self):
        self.way.currentTextChanged.connect(self.cheq_num_on_off)
        self.type.currentTextChanged.connect(self.get_code)
        self.code_input.valueChanged.connect(self.get_type)

    def get_data(self):
        return {
            "name": self.name.text(),
            "date": self.date.date().toPyDate(),
            "code_input": self.code_input.value(),
            "type": self.type.currentText(),
            "way": self.way.currentText(),
            "bill_number": self.bill_number.text(),
            "cheq_num": self.nb_cheque.text(),
            "bank_caisse": self.bank_caisse.currentText(),
            "price": self.price.value(),
            "note": self.note.text(),
        }
        
    def repopulate_fields(self, data: dict) -> None:
        self.name.setText(data.get("name", ""))
        self.date.setDate(data.get("date", self.date.date()))
        self.code_input.setValue(data.get("code_input", 0))
        self.type.setCurrentText(data.get("type", ""))
        self.way.setCurrentText(data.get("way", ""))
        self.bill_number.setText(data.get("bill_number", ""))
        self.nb_cheque.setText(data.get("nb_cheque", ""))
        self.bank_caisse.setCurrentText(data.get("bank_caisse", ""))
        self.price.setValue(data.get("price", 0.0))
        self.note.setText(data.get("note", ""))
        
        self.bank_caisse.setEnabled(False)
        
    def populate_combos(self) -> None:
        self.combo_manager.update_combo(self.type, ComboName.INCOME)
        self.combo_manager.update_combo(self.way, ComboName.WAY_PAYMENT)
        
    def cheq_num_on_off(self):
        if self.way.currentText() == "صك":
            self.nb_cheque.setEnabled(True)
        else:
            self.nb_cheque.setEnabled(False)
            
    def get_code(self):
        expense_type = self.settings_manager.get_code(income=self.type.currentText(), expense=None)
        if expense_type is None:
            self.code_input.setValue(0)
        else:
            self.code_input.setValue(expense_type)
            
    def get_type(self):
        code = self.settings_manager.get_type(income_code=self.code_input.value(), expense_code=None)
        if code is None:
            self.type.setCurrentIndex(-1)
        else:
            self.type.setCurrentText(code[0])

class PaymentForm(QWidget, AddPaymentUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.PAYMENTS, "add_payment.ui", self)

        self.model = None
        self.identifier = 0
        self.momentane: list[EntrySchema] = []
        
        self.student_manager = get_model(ModelName.STUDENT)
        self.manager = get_model(ModelName.PAYMENTS)
        self.combo_manager = get_combo_manager()
        self.enrollment_manager = get_model(ModelName.ENROLLMENT)
        self.classes_manager = get_model(ModelName.CLASSES)

        self.date.setDate(QDate.currentDate())
        self.addition_date.setDate(QDate.currentDate())

        self.setup_student_search()
        self.cheq_num_on_off()
        self.populate_combo()
        self.setup()
        self.show_bill()

    def setup(self):
        self.add_btn.clicked.connect(self.control)
        self.reset_btn.clicked.connect(self.reset)
        self.confirm_btn.clicked.connect(self.confirm_bill)
        self.bill_tbl.doubleClicked.connect(self.delete_from_bill)
        self.student_list.doubleClicked.connect(self.select_student)
        self.search_student.textChanged.connect(self.search_student_func)
        self.way.currentTextChanged.connect(self.cheq_num_on_off)
        self.classroom.currentTextChanged.connect(lambda: self.set_price(self.classroom.currentText()))

    def setup_student_search(self):
        self.model = create_table_model(TableType.STUDENT_SEARCH)

        self.student_list.setModel(self.model)
        self.student_list.hideColumn(self.model.ID_COLUMN)

    def search_student_func(self, name = None):
        name = None if name == "" else name
        
        students = get_student_list(name)

        self.model.refresh(students)

        self.student_list.repaint()
        
    def select_student(self, index):
        row = index.row()
        print(row)
        if not row:
            error("يرجى تحديد التلميذ")
            return
        
        self.identifier = self.model.data(self.model.index(row, 0), role=0)
        name = self.model.data(self.model.index(row, 1), role=0)  

        self.student_list.clearSelection()

        self.name.setText(str(name))
        self.populate_classes(self.identifier)
        self.note_payment()

    def note_payment(self):
        student = self.student_manager.get_by_id(self.identifier)
        note = student.note
        if note: 
            info(note)

    def control(self):
        name = self.name.text()
        classroom = self.classroom.currentText()
        price = self.price.text()
        date = self.date.date()
        way = self.way.currentText()
        cheq_num = self.cheq_num.text()
        bill_number = self.bill_number.text()
        addition_date = self.addition_date.date()

        entity = SchemaFactory.INCOME(
            num_inscrit=self.identifier,
            name=name,
            classroom=classroom,
            price=price,
            payment_date=date.toPyDate(),
            way=way,
            cheq_num=cheq_num,
            bill_number=bill_number,
            addition_date=addition_date.toPyDate(),
            type="تسجيل",
            code=13,
            note="",
            user=get_username(),
            in_bank=False
        )

        try:
            if not entity.validate():
                error("الرجاء ملء جميع الحقول")
                return
        except ValueError as e:
            error(str(e))
            return
        
        if self.is_unique(self.identifier, classroom, date):
            error("تم تسجيل هذا الدفع مسبقا")
            return
        self.add(entity)

    def add(self, data):
        self.momentane.append(data)

        self.show_bill()

    def delete_from_bill(self, row):
        self.momentane.pop(row.row())

        self.show_bill()

    def show_bill(self):
        self.bill_tbl.setRowCount(len(self.momentane))

        for i in range(len(self.momentane)):
            row = self.momentane[i]
            self.bill_tbl.setItem(i, 0, QTableWidgetItem(str(row.num_inscrit)))
            self.bill_tbl.setItem(i, 1, QTableWidgetItem(str(row.name)))
            self.bill_tbl.setItem(i, 2, QTableWidgetItem(str(row.classroom)))
            self.bill_tbl.setItem(i, 3, QTableWidgetItem(str(row.price)))
            self.bill_tbl.setItem(i, 4, QTableWidgetItem(str(row.payment_date.strftime("%Y-%m"))))
            self.bill_tbl.setItem(i, 5, QTableWidgetItem(str(row.way)))
            self.bill_tbl.setItem(i, 6, QTableWidgetItem(str(row.addition_date.strftime("%Y-%m-%d"))))

    def confirm_bill_security(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("هل تريد تاكيد الفاتورة؟")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.confirm_bill()

    def confirm_bill(self):

        try:
            for row in self.momentane:
                self.manager.create(row)

            info("تمت إضافة الفاتورة بنجاح")
        except Exception as e:
            print(e)
            self.manager.rollback()
        finally:
            self.momentane = []
            self.reset()
            self.show_bill()


    def populate_combo(self):
        self.combo_manager.update_combo(self.way, ComboName.WAY_PAYMENT)

    def populate_classes(self, identifier): 
        filters = self.enrollment_manager.get_filters(student_id=identifier)
        enrollments = self.enrollment_manager.get_by_filter(filters)
        class_names = [enrollment.class_name for enrollment in enrollments]

        self.combo_manager.update_with_data(self.classroom, class_names)  
    
    def reset(self):
        self.name.setText("")
        self.classroom.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.price.setValue(0)
        self.cheq_num.setText("")
        self.date.setDate(QDate.currentDate())
        self.identifier = 0

    def set_price(self, classroom):
        if classroom != "":
            filter = self.classes_manager.get_filters(name=classroom)
            class_ = self.classes_manager.get_by_filter(filter)
            price = class_[0].price if class_ else 0
            self.price.setValue(price)

    def is_unique(self, identifier, classroom, date):

        # Checking for payment with the same identifier, classroom, and matching year and month
        if classroom == "تأمين":
            filters = self.manager.get_filter(
                num_inscrit=identifier,
                classroom=classroom,
                year=date.year()  # Use exact date for "تأمين" payments
            )
            
            # If payment exists and classroom is "تأمين", check if the year is different
            return self.manager.exists(filters)  # It's not unique if same identifier, classroom, and year
        else:
            filters = self.manager.get_filter(
                num_inscrit=identifier,
                classroom=classroom,
                year=date.year(),
                month=date.month()
            )

        # Check in momentane for non-database temporary data
        if len(self.momentane) > 0:
            for i in self.momentane:
                if i.classroom == "تأمين" and classroom == "تأمين":
                    if i.payment_date.year == date.year():
                        return True
                else:
                    if i.num_inscrit == identifier and i.classroom == classroom and i.payment_date.year == date.year() and i.payment_date.month == date.month():
                        return True

        return False  # If no match, it's unique
    
    def cheq_num_on_off(self):
        if self.way.currentText() == "صك":
            self.cheq_num.setEnabled(True)
        else:
            self.cheq_num.setEnabled(False)

