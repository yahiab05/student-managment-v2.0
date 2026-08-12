from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableView,
    QTableWidget,
    QTextEdit,
    QWidget,
)


class LoginUI:
    login: QWidget
    username: QLineEdit
    password: QLineEdit
    submit: QPushButton


class MainUI:
    main_app: QMainWindow
    centralwidget: QWidget
    username: QLabel
    log_out: QPushButton
    user: QPushButton
    settings: QPushButton
    absents: QPushButton
    money: QPushButton
    payment: QPushButton
    teachers: QPushButton
    classes: QPushButton
    students: QPushButton
    stackedWidget: QStackedWidget


class ClassPartUI:
    class_part: QWidget
    classeleve: QPushButton
    classes: QPushButton
    stackedWidget: QStackedWidget


class ClasseleveUI:
    classeleve: QWidget
    classeleve_stacked: QStackedWidget
    nb: QLabel
    classes: QComboBox
    students: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    clear_class: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    printing_plain: QTextEdit
    cancel: QPushButton
    printing_unpayed: QPushButton
    student_search: QLineEdit
    student_search_list: QTableView


class ClassesUI:
    classes_widget: QWidget
    nb: QLabel
    teacher_search: QComboBox
    search: QLineEdit
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    class_table: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton


class ClassesPerStudentUI:
    class_per_student: QWidget
    class_list: QListWidget
    search_ent: QLineEdit
    student_list: QTableView
    reset_btn: QPushButton


class CaisseUI:
    caisse: QWidget
    stackedWidget: QStackedWidget
    total_caisse: QLabel
    total_bank: QLabel
    price_search: QDoubleSpinBox
    operatore: QComboBox
    to: QDateEdit
    du: QDateEdit
    table: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    vider: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    date: QDateEdit
    price: QDoubleSpinBox
    note: QLineEdit
    to_bank_btn: QPushButton
    to_caisse_btn: QPushButton
    printing_plain: QTextEdit
    cancel: QPushButton
    printing: QPushButton


class EnteryMoneyUI:
    enterymoney: QWidget
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    tbl: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    bill_code: QLineEdit
    name_search: QLineEdit
    price_search: QDoubleSpinBox
    operatore: QComboBox
    to: QDateEdit
    du: QDateEdit
    code: QSpinBox
    type_search: QComboBox
    way_search: QComboBox
    total: QLabel
    reset_btn: QPushButton
    search_btn: QPushButton


class MoneyUI:
    money: QWidget
    bank: QPushButton
    caisse: QPushButton
    solde: QPushButton
    out_money: QPushButton
    add_money: QPushButton
    stackedWidget: QStackedWidget


class OutMoneyUI:
    outmoney: QWidget
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    tbl: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    name_search: QComboBox
    price_search: QDoubleSpinBox
    operatore: QComboBox
    to: QDateEdit
    du: QDateEdit
    way_search: QComboBox
    code: QSpinBox
    type_search: QComboBox
    total: QLabel
    reset_btn: QPushButton
    search_btn: QPushButton


class BalanceUI:
    soldeform: QWidget
    tbl: QTableView
    solde: QLabel
    total_in: QLabel
    total_out: QLabel
    printing_btn: QPushButton
    export_btn: QPushButton
    price_input: QDoubleSpinBox
    operatore: QComboBox
    du: QDateEdit
    to: QDateEdit
    way: QComboBox
    reset_btn: QPushButton
    search_btn: QPushButton


class TransferUI:
    caisse: QWidget
    stackedWidget: QStackedWidget
    total_caisse: QLabel
    total_bank: QLabel
    price_search: QDoubleSpinBox
    operatore: QComboBox
    to: QDateEdit
    du: QDateEdit
    table: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    vider: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    date: QDateEdit
    price: QDoubleSpinBox
    note: QLineEdit
    to_bank_btn: QPushButton
    to_caisse_btn: QPushButton
    printing_plain: QTextEdit
    cancel: QPushButton
    printing: QPushButton


class ClassesFormUI:
    Form: QWidget
    note: QLineEdit
    way: QComboBox
    price: QLineEdit
    name: QLineEdit
    teacher: QComboBox


class ExpensesFormUI:
    Form: QWidget
    price: QDoubleSpinBox
    bill_num: QLineEdit
    way: QComboBox
    code_input: QSpinBox
    date: QDateEdit
    type: QComboBox
    bank_caisse: QComboBox
    note: QLineEdit
    nb_cheque: QLineEdit
    name: QComboBox


class IncomeFormUI:
    Form: QWidget
    name: QLineEdit
    date: QDateEdit
    code_input: QSpinBox
    type: QComboBox
    way: QComboBox
    bill_number: QLineEdit
    nb_cheque: QLineEdit
    bank_caisse: QComboBox
    price: QDoubleSpinBox
    note: QLineEdit


class PopupFormUI:
    Form: QWidget
    title: QLabel
    widget: QWidget
    cancel_btn: QPushButton
    confirm_btn: QPushButton


class SettingFormUI:
    Form: QWidget
    title: QLabel
    nb: QLabel
    entery: QLineEdit
    list: QListWidget
    add_btn: QPushButton
    reset_btn: QPushButton
    update_btn: QPushButton
    delete_btn: QPushButton


class SettingWithCodeFormUI:
    Form: QWidget
    title: QLabel
    nb: QLabel
    code: QSpinBox
    entery: QLineEdit
    list: QTableWidget
    add_btn: QPushButton
    reset_btn: QPushButton
    entery_update_btn: QPushButton
    entery_delete_btn: QPushButton


class StudentFormUI:
    Form: QWidget
    activity: QComboBox
    birthday: QDateEdit
    excused: QComboBox
    parent_ent: QLineEdit
    gender: QComboBox
    note: QLineEdit
    date_inscrit: QDateEdit
    num_tel_2: QLineEdit
    name: QLineEdit
    num_tel: QLineEdit
    cin: QLineEdit


class TeacherFormUI:
    Form: QWidget
    name: QLineEdit
    date_inscrit: QDateEdit
    birthday: QDateEdit
    phone: QLineEdit
    phone_2: QLineEdit
    note: QLineEdit


class RoleUI:
    role_form: QWidget
    reset_btn: QPushButton
    search_btn: QPushButton
    name_search: QComboBox
    name: QLineEdit
    students: QCheckBox
    teachers: QCheckBox
    classes: QCheckBox
    payment: QCheckBox
    absents: QCheckBox
    money: QCheckBox
    settings: QCheckBox
    user: QCheckBox
    payment_edit: QCheckBox
    delete_btn: QPushButton
    add_btn: QPushButton
    update_btn: QPushButton
    new_btn: QPushButton
    all_btn: QPushButton


class SettingsUI:
    teacher: QWidget
    fr_btn: QPushButton
    payment_btn: QPushButton
    expense_btn: QPushButton
    income_btn: QPushButton
    way_btn: QPushButton
    plane: QStackedWidget


class UserUI:
    users: QWidget
    role: QComboBox
    passwd: QLineEdit
    user: QLineEdit
    tbl: QTableWidget
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    new_btn: QPushButton


class UserPartUI:
    user_part: QWidget
    add_role: QPushButton
    user: QPushButton
    stackedWidget: QStackedWidget


class AddPaymentUI:
    Form: QWidget
    name: QLabel
    classroom: QComboBox
    way: QComboBox
    bill_number: QLineEdit
    cheq_num: QLineEdit
    price: QDoubleSpinBox
    addition_date: QDateEdit
    date: QDateEdit
    confirm_btn: QPushButton
    reset_btn: QPushButton
    add_btn: QPushButton
    bill_tbl: QTableWidget
    search_student: QLineEdit
    student_list: QTableView


class PaymentPartUI:
    Form: QWidget
    view_not_payed: QPushButton
    view_payment: QPushButton
    stackedWidget: QStackedWidget


class ViewNotPayedUI:
    Form: QWidget
    tbl: QListWidget
    classroom: QComboBox
    month: QSpinBox
    year: QSpinBox
    reset_btn: QPushButton
    search_btn: QPushButton


class ViewPaymentUI:
    view_payment: QWidget
    stackedWidget: QStackedWidget
    page: QWidget
    edit_btn: QPushButton
    delete_btn: QPushButton
    add_btn: QPushButton
    reg_tbl: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    nb: QLabel
    total: QLabel
    page_2: QWidget
    previous_price: QLabel
    new_price: QDoubleSpinBox
    cancel_btn: QPushButton
    update_btn: QPushButton
    search_frame: QFrame
    search_ent: QLineEdit
    student_list: QListWidget
    num_inscrit: QLineEdit
    classroom: QComboBox
    way: QComboBox
    du: QDateEdit
    to: QDateEdit
    reset_btn: QPushButton
    search_btn: QPushButton


class StudentHistoryUI:
    student_history: QWidget
    num_ins_search: QLineEdit
    student_tab: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton


class StudentPartUI:
    student_part: QWidget
    classes_per_student: QPushButton
    students_history: QPushButton
    students: QPushButton
    stackedWidget: QStackedWidget


class StudentsUI:
    students: QWidget
    search_by_name: QLineEdit
    maximize: QPushButton
    new_year: QPushButton
    new_btn: QPushButton
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    student_tab: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    search_frame: QFrame
    minimize: QPushButton
    du: QDateEdit
    to: QDateEdit
    excused_search: QComboBox
    activity_search: QComboBox
    gender_search: QComboBox
    nb: QLabel


class TeacherUI:
    Form: QWidget
    nb: QLabel
    search: QLineEdit
    new_year_btn: QPushButton
    update_btn: QPushButton
    delete_btn: QPushButton
    add_btn: QPushButton
    teachers_table: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton


class TeacherHistoryUI:
    teacher_history: QWidget
    nb: QLabel
    search: QLineEdit
    history_table: QTableView
    printing_btn: QPushButton
    export_btn: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton


class TeacherPartUI:
    teacher_part: QWidget
    teacher_history: QPushButton
    teacher: QPushButton
    stackedWidget: QStackedWidget