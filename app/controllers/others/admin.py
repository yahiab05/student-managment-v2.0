from PyQt6.QtWidgets import QTableWidgetItem, QWidget

from app.ui.ui_forms import RoleUI, UserUI
from app.utils import error, get_combo_manager, WorkingMode, ComboName, load_gui, UiPath
from app.repo.schemas import SchemaFactory
from app.models import get_model, ModelName

class RoleLogic(QWidget, RoleUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.OTHERS, "role.ui", self)

        self.manager = get_model(ModelName.ROLES)
        self.user_manager = get_model(ModelName.USERS)
        self.combo_manager = get_combo_manager()

        self.name_selected = ""
        self.populate_combo()

        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.select_role)
        self.reset_btn.clicked.connect(self.reset)
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.control(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete_role)
        self.all_btn.clicked.connect(self.select_deselect_all)

    def control(self, action:WorkingMode):
        role = self.name.text()
        students = self.students.isChecked()
        teachers = self.teachers.isChecked()
        classes = self.classes.isChecked()
        payment = self.payment.isChecked()
        absents = self.absents.isChecked()
        money = self.money.isChecked()
        settings = self.settings.isChecked()
        user = self.user.isChecked()
        payment_edit = self.payment_edit.isChecked()
        
        entity = SchemaFactory.ROLE(
            name=role,
            students=students,
            teachers=teachers,
            classes=classes,
            payment=payment,
            absent=absents,
            money=money,
            settings=settings,
            user=user,
            payment_editting=payment_edit
        )
        
        try:
            if not entity.validate():
                error("الرجاء التحقق من صحة البيانات")
                return
        except ValueError as e:
            print(f"Validation error: {e}")
            error(str(e))
            return

        if action == WorkingMode.ADD:
            self.manager.create(entity)
        else:
            if self.name_selected:
                filters = self.manager.get_filter(role_name=self.name_selected)
                self.manager.update_by_filter(filters, entity)
            else:
                error("يرجى تحديد دور")
        self.combo_manager.update_cache_from_db(ComboName.ROLE)

    def select_role(self):
        if self.name_search.currentText():
            self.name_selected = self.name_search.currentText()

            filters = self.manager.get_filter(role_name=self.name_selected)

            data = self.manager.get_by_filter(filters)

            if len(data) > 0:
                role = data[0]

                self.students.setChecked(role.students)
                self.teachers.setChecked(role.teachers)
                self.classes.setChecked(role.classes)
                self.payment.setChecked(role.payment)
                self.money.setChecked(role.money)
                self.settings.setChecked(role.settings)
                self.user.setChecked(role.user)
                self.payment_edit.setChecked(role.payment_editting)

    def delete_role(self):
        filters = self.user_manager.get_filter(role=self.name_selected)
        users_with_role = self.user_manager.get_by_filter(filters)
        if len(users_with_role) > 0:
            error("لا يمكن حذف هذا الدور لأنه مرتبط بمستخدمين")
            return
        if self.name_selected:
            filters = self.manager.get_filter(role_name=self.name_selected)
            self.manager.sup_security(text= "متأكد من حذف هذا الدور ؟", filter=filters)
            self.combo_manager.update_cache_from_db(ComboName.ROLE)
        else:
            error("يرجى تحديد دور")      

    def populate_combo(self):
        self.combo_manager.update_combo(self.name_search, ComboName.ROLE)

    def reset(self):
        self.name_selected = ""
        self.name.setText("")
        self.name_search.setCurrentIndex(-1)
        self.students.setChecked(False)
        self.teachers.setChecked(False)
        self.classes.setChecked(False)
        self.payment.setChecked(False)
        self.absents.setChecked(False)
        self.money.setChecked(False)
        self.settings.setChecked(False)
        self.user.setChecked(False)
        self.payment_edit.setChecked(False)

    def select_deselect_all(self):
        self.students.setChecked(True)
        self.teachers.setChecked(True)
        self.classes.setChecked(True)
        self.payment.setChecked(True)
        self.absents.setChecked(True)
        self.money.setChecked(True)
        self.settings.setChecked(True)
        self.user.setChecked(True)
        self.payment_edit.setChecked(True)

class UserLogic(QWidget, UserUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_gui(UiPath.OTHERS, "user.ui", self)
        
        self.manager = get_model(ModelName.USERS)
        self.combo_manager = get_combo_manager()
        
        self.identifier = None

        self.show_users()
        self.populate_combo()
        self.setup()

    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control(WorkingMode.ADD))
        self.update_btn.clicked.connect(lambda: self.control(WorkingMode.UPDATE))
        self.delete_btn.clicked.connect(self.delete)
        self.tbl.clicked.connect(self.select_user)

    def reset(self):
        self.user.setText('')
        self.passwd.setText('')
        self.role.setCurrentIndex(-1)

    def control(self, action: WorkingMode):
        username = self.user.text()
        password = self.passwd.text()
        role = self.role.currentText()
        
        entity = SchemaFactory.USER(
            username=username,
            password=password,
            role_name=role
        )
        
        try:
            if not entity.validate():
                error("الرجاء التحقق من صحة البيانات")
                return
        except ValueError as e:
            error(str(e))
            print(f"Validation error: {e}")
            return
        
        if action == WorkingMode.ADD:
            self.manager.create(entity)
        else:
            if self.identifier:
                self.manager.update(self.identifier, entity)
                self.identifier = None
            else:
                error("يرجى تحديد مستخدم")
        self.show_users()
        self.reset()
    
    def select_user(self):
        row = self.tbl.currentRow()
        self.identifier = self.tbl.item(row, 0).text()

        user = self.tbl.item(row, 0).text()
        password = self.tbl.item(row, 1).text()
        role = self.tbl.item(row, 2).text()

        self.user.setText(user)
        self.passwd.setText(password)
        self.role.setCurrentText(role)

    def delete(self):
        if not self.identifier:
            error("يرجى تحديد مستخدم")
            return
        
        self.manager.sup_security(id=self.identifier, text="متأكد من حذف هذا المستخدم ؟")
        self.show_users()
        self.reset()
        self.identifier = None

    def show_users(self):
        users = self.manager.get_all()

        for i in range(len(users)):
            user = users[i]
            self.tbl.setItem(i, 0, QTableWidgetItem(str(user.id)))
            self.tbl.setItem(i, 1, QTableWidgetItem(user.username))
            self.tbl.setItem(i, 2, QTableWidgetItem(user.password))
            self.tbl.setItem(i, 3, QTableWidgetItem(user.role_name))

    def populate_combo(self):
        self.combo_manager.update_combo(self.role, ComboName.ROLE)

