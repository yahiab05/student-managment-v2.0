from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QDate
from sqlalchemy.exc import IntegrityError

from app.ui.ui_forms import ViewPaymentUI as V
from app.view import create_table_model, TableType
from app.models import get_model, ModelName
from app.utils import (error, get_student_list, get_combo_manager, ComboName, 
                        ReportType, load_gui, UiPath, traceback_to_string, get_selection_status_stylesheet)
from app.controllers.popup import create_payment_window

class ViewPayment(QWidget, V):
    def __init__(self):
        super().__init__()

        load_gui(UiPath.PAYMENTS, "view_payment.ui", self)  

        self.to.setDate(QDate.currentDate())
        self.du.setDate(QDate(2000, 1, 1))

        self.identifier = 0
        
        self.manager = get_model(ModelName.PAYMENTS)
        self.combo_manager = get_combo_manager

        self.setup_table()
        self.setup()
        
        self.show_students_list()
        self.deselection()

    def setup(self):
        self.add_btn.clicked.connect(self.open_popup)
        self.edit_btn.clicked.connect(self.set_old_price)
        self.delete_btn.clicked.connect(self.delete)
        self.search_ent.textChanged.connect(lambda: self.show_students_list(self.search_ent.text()))
        self.student_list.itemDoubleClicked.connect(self.select_student)
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(self.reset)
        self.reg_tbl.doubleClicked.connect(self.select_row)
        self.update_btn.clicked.connect(self.edit_price) 
        self.cancel_btn.clicked.connect(self.cancel)
        self.printing_btn.clicked.connect(lambda: self.export(ReportType.PRINT))
        self.export_btn.clicked.connect(lambda: self.export(ReportType.EXCEL))

    def setup_table(self):
        self.model = create_table_model(TableType.PAYMENT)

        self.reg_tbl.setModel(self.model)

        self.total.setText(str(self.manager.get_total()))
        self.nb.setText(str(self.model.rowCount()))
        
    def open_popup(self):
        popup = create_payment_window(self)
        popup.show()

    def search(self):
        student = self.search_ent.text() if self.search_ent.text() != "" else None
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        classroom = self.classroom.currentText() if self.classroom.currentText() != "" else None
        num_inscrit = self.num_inscrit.text() if self.num_inscrit.text() != "" else None
        way = self.way.currentText() if self.way.currentText() != "" else None

        filters = self.manager.get_filter(
            classroom=classroom,
            name=student,
            way=way,
            payment_from_date=from_date,
            payment_to_date=to_date,
            num_inscrit=num_inscrit
        )
        
        data = self.manager.get_by_filter(filters)

        self.model.refresh(data)
        self.reg_tbl.repaint()

        self.total.setText(str(self.manager.get_total(filters)))
        self.nb.setText(str(self.model.rowCount()))

    def select_student(self):
        name = self.student_list.currentItem().text()

        self.search_ent.setText(name)

    def show_students_list(self, student = ""):
        students = get_student_list(student)
        self.student_list.clear()
        for s in students:
            self.student_list.addItem(s.name)

    def reset(self):
        self.search_ent.setText("")
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())
        self.classroom.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.num_inscrit.setText("")

        self.show_students_list()
        
    def selection(self, identifier):
        self.identifier = identifier
        self.select_info.setStyleSheet(get_selection_status_stylesheet(True))
        
    def deselection(self):
        self.identifier = None
        self.select_info.setStyleSheet(get_selection_status_stylesheet(False))

    def select_row(self, index):
        if self.has_access():
            row_index = index.row()
            
            identifier = self.model.data(self.model.index(row_index, 0), role=0)
            self.selection(identifier)

            self.reg_tbl.clearSelection()
            self.search_frame.setEnabled(False)
        else:
            error("ليس لديك صلاحية")

    def set_old_price(self):
        if self.identifier is not None:
            print(self.identifier)
            old_payment = self.manager.get_by_id(self.identifier)

            print(old_payment.price)
            self.previous_price.setText(str(old_payment.price))  
            self.stackedWidget.setCurrentIndex(1)
        else:
            error("الرجاء اختيار الدفع الذي تريد تعديله")

    def has_access(self):
        access_manager = get_model(ModelName.ACCESS)
        return access_manager.get_access("payment_edit")

    def edit_price(self):
        if self.new_price.value() > 0:
            try:
                self.manager.update_price(self.identifier, self.new_price.value())
            except Exception as e:
                print(e)
                error("لا يمكنك التحديث بعد الآن")
            finally:
                self.cancel()
                self.deselection()
                self.search()
        else:
            error("السعر يجب ان يكون اكبر من صفر")

    def cancel(self):
        self.stackedWidget.setCurrentIndex(0)
        self.new_price.setValue(0)
        self.previous_price.setText("")
        self.search_frame.setEnabled(True)

    def populate_combos(self):
        self.combo_manager.update_combo(self.way, ComboName.WAY_PAYMENT)
        self.combo_manager.update_combo(self.classroom, ComboName.CLASS)
        
    def delete(self):
        try:
            self.manager.sup_security(widget=self, id=self.identifier, text="متأكد من حذف هذا الدفعة ؟")
            self.deselection()
            self.search()
            self.search_frame.setEnabled(True)
        except IntegrityError as e:
            print(traceback_to_string(e))
            error("لا يمكنك حذف هذا الدفعة")
        
    def export(self, output_channel: ReportType):
        data = self.model.get_current_data()
        total = self.manager.get_total()
        self.manager.set_dynamic_metadata(
            data_to_export=data,
            total_price=total
        )
        
        self.manager.export_data(
            report_type=output_channel, 
            parent=self
        )