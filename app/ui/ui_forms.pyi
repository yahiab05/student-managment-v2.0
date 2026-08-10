from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QFrame,
    QGroupBox,
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
    frame: QFrame
    label: QLabel
    frame_3: QFrame
    frame_2: QFrame
    username: QLineEdit
    password: QLineEdit
    frame_4: QFrame
    submit: QPushButton


class MainUI:
    main_app: QMainWindow
    centralwidget: QWidget
    frame: QFrame
    username: QLabel
    label: QLabel
    log_out: QPushButton
    frame_2: QFrame
    frame_3: QFrame
    user: QPushButton
    settings: QPushButton
    absents: QPushButton
    money: QPushButton
    payment: QPushButton
    teachers: QPushButton
    classes: QPushButton
    students: QPushButton
    stackedWidget: QStackedWidget
    page: QWidget
    label_2: QLabel


class ClassPartUI:
    class_part: QWidget
    frame: QFrame
    classeleve: QPushButton
    classes: QPushButton
    stackedWidget: QStackedWidget


class ClasseleveUI:
    classeleve: QWidget
    frame_2: QFrame
    classeleve_stacked: QStackedWidget
    stackedWidget_4Page1: QWidget
    frame_5: QFrame
    nb: QLabel
    label_8: QLabel
    classes: QComboBox
    students: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    clear_class: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    page: QWidget
    frame_18: QFrame
    printing_plain: QTextEdit
    frame_19: QFrame
    cancel: QPushButton
    printing_unpayed: QPushButton
    frame_3: QFrame
    student_search: QLineEdit
    student_search_list: QTableView


class ClassesUI:
    classes_widget: QWidget
    frame_3: QFrame
    frame_2: QFrame
    nb: QLabel
    label_8: QLabel
    teacher_search: QComboBox
    label_9: QLabel
    search: QLineEdit
    label_7: QLabel
    frame: QFrame
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    class_table: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton


class ClassesPerStudentUI:
    class_per_student: QWidget
    frame_2: QFrame
    label_17: QLabel
    class_list: QListWidget
    frame_4: QFrame
    search_ent: QLineEdit
    student_list: QTableView
    reset_btn: QPushButton


class CaisseUI:
    caisse: QWidget
    stackedWidget: QStackedWidget
    stackedWidgetPage1: QWidget
    frame_11: QFrame
    total_caisse: QLabel
    label_21: QLabel
    total_bank: QLabel
    label_19: QLabel
    frame: QFrame
    frame_3: QFrame
    frame_5: QFrame
    price_search: QDoubleSpinBox
    operatore: QComboBox
    label_7: QLabel
    frame_2: QFrame
    to: QDateEdit
    label_8: QLabel
    du: QDateEdit
    label_9: QLabel
    table: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    vider: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    frame_4: QFrame
    frame_6: QFrame
    date: QDateEdit
    label_2: QLabel
    frame_8: QFrame
    price: QDoubleSpinBox
    label_5: QLabel
    frame_10: QFrame
    note: QLineEdit
    label_6: QLabel
    frame_12: QFrame
    to_bank_btn: QPushButton
    to_caisse_btn: QPushButton
    page: QWidget
    printing_plain: QTextEdit
    frame_19: QFrame
    cancel: QPushButton
    printing: QPushButton


class EnteryMoneyUI:
    enterymoney: QWidget
    frame_6: QFrame
    label_13: QLabel
    frame_18: QFrame
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    tbl: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    bill_code: QLineEdit
    frame: QFrame
    frame_9: QFrame
    name_search: QLineEdit
    label_18: QLabel
    frame_2: QFrame
    price_search: QDoubleSpinBox
    operatore: QComboBox
    label_7: QLabel
    frame_4: QFrame
    to: QDateEdit
    label_8: QLabel
    du: QDateEdit
    label_9: QLabel
    frame_8: QFrame
    code: QSpinBox
    label_12: QLabel
    type_search: QComboBox
    label_10: QLabel
    frame_10: QFrame
    way_search: QComboBox
    label_11: QLabel
    frame_11: QFrame
    total: QLabel
    label_17: QLabel
    frame_5: QFrame
    reset_btn: QPushButton
    search_btn: QPushButton


class MoneyUI:
    money: QWidget
    frame: QFrame
    frame_4: QFrame
    bank: QPushButton
    caisse: QPushButton
    label: QLabel
    frame_2: QFrame
    solde: QPushButton
    out_money: QPushButton
    add_money: QPushButton
    stackedWidget: QStackedWidget


class OutMoneyUI:
    outmoney: QWidget
    frame_2: QFrame
    frame: QFrame
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    tbl: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    frame_4: QFrame
    frame_10: QFrame
    name_search: QComboBox
    label_16: QLabel
    frame_5: QFrame
    price_search: QDoubleSpinBox
    operatore: QComboBox
    label_7: QLabel
    frame_8: QFrame
    to: QDateEdit
    label_8: QLabel
    du: QDateEdit
    label_9: QLabel
    frame_11: QFrame
    way_search: QComboBox
    label_11: QLabel
    frame_9: QFrame
    code: QSpinBox
    label_12: QLabel
    type_search: QComboBox
    label_10: QLabel
    frame_12: QFrame
    total: QLabel
    label_17: QLabel
    frame_13: QFrame
    reset_btn: QPushButton
    search_btn: QPushButton


class SoldeFormUI:
    soldeform: QWidget
    frame_10: QFrame
    frame_3: QFrame
    tbl: QTableView
    frame_11: QFrame
    solde: QLabel
    label_20: QLabel
    total_in: QLabel
    label_21: QLabel
    total_out: QLabel
    label_19: QLabel
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    frame_4: QFrame
    frame_9: QFrame
    price_input: QDoubleSpinBox
    operatore: QComboBox
    label_7: QLabel
    frame_6: QFrame
    du: QDateEdit
    label_9: QLabel
    frame_5: QFrame
    to: QDateEdit
    label_8: QLabel
    frame_2: QFrame
    way: QComboBox
    label_11: QLabel
    frame_32: QFrame
    reset_btn: QPushButton
    search_btn: QPushButton


class TransferUI:
    caisse: QWidget
    stackedWidget: QStackedWidget
    stackedWidgetPage1: QWidget
    frame_11: QFrame
    total_caisse: QLabel
    label_21: QLabel
    total_bank: QLabel
    label_19: QLabel
    frame: QFrame
    frame_3: QFrame
    frame_5: QFrame
    price_search: QDoubleSpinBox
    operatore: QComboBox
    label_7: QLabel
    frame_2: QFrame
    to: QDateEdit
    label_8: QLabel
    du: QDateEdit
    label_9: QLabel
    table: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    vider: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    frame_4: QFrame
    frame_6: QFrame
    date: QDateEdit
    label_2: QLabel
    frame_8: QFrame
    price: QDoubleSpinBox
    label_5: QLabel
    frame_10: QFrame
    note: QLineEdit
    label_6: QLabel
    frame_12: QFrame
    to_bank_btn: QPushButton
    to_caisse_btn: QPushButton
    page: QWidget
    printing_plain: QTextEdit
    frame_19: QFrame
    cancel: QPushButton
    printing: QPushButton


class ClassesFormUI:
    Form: QWidget
    note: QLineEdit
    label_5: QLabel
    way: QComboBox
    label_3: QLabel
    price: QLineEdit
    label_6: QLabel
    name: QLineEdit
    label_2: QLabel
    teacher: QComboBox
    label_4: QLabel


class ExpensesFormUI:
    Form: QWidget
    frame_4: QFrame
    price: QDoubleSpinBox
    bill_num: QLineEdit
    label_19: QLabel
    way: QComboBox
    code_input: QSpinBox
    date: QDateEdit
    label_2: QLabel
    type: QComboBox
    label_14: QLabel
    bank_caisse: QComboBox
    label_6: QLabel
    label_15: QLabel
    note: QLineEdit
    label_18: QLabel
    nb_cheque: QLineEdit
    label_13: QLabel
    label_4: QLabel
    label_3: QLabel
    label_5: QLabel
    name: QComboBox


class IncomeFormUI:
    Form: QWidget
    frame_4: QFrame
    frame: QFrame
    name: QLineEdit
    label_16: QLabel
    frame_2: QFrame
    date: QDateEdit
    label_2: QLabel
    frame_8: QFrame
    code_input: QSpinBox
    label_19: QLabel
    frame_9: QFrame
    type: QComboBox
    label_3: QLabel
    frame_10: QFrame
    way: QComboBox
    label_4: QLabel
    frame_12: QFrame
    bill_number: QLineEdit
    label_20: QLabel
    frame_11: QFrame
    nb_cheque: QLineEdit
    label_15: QLabel
    frame_13: QFrame
    bank_caisse: QComboBox
    label_13: QLabel
    frame_14: QFrame
    price: QDoubleSpinBox
    label_5: QLabel
    frame_15: QFrame
    note: QLineEdit
    label_6: QLabel


class PopupFormUI:
    Form: QWidget
    title: QLabel
    widget: QWidget
    frame: QFrame
    delete_btn: QPushButton
    add_btn: QPushButton


class SettingFormUI:
    Form: QWidget
    title: QLabel
    frame_6: QFrame
    nb: QLabel
    entery: QLineEdit
    list: QListWidget
    frame_14: QFrame
    add_btn: QPushButton
    reset_btn: QPushButton
    frame_13: QFrame
    update_btn: QPushButton
    delete_btn: QPushButton


class SettingWithCodeFormUI:
    Form: QWidget
    frame_7: QFrame
    title: QLabel
    frame: QFrame
    nb: QLabel
    code: QSpinBox
    entery: QLineEdit
    list: QTableWidget
    frame_8: QFrame
    add_btn: QPushButton
    reset_btn: QPushButton
    frame_12: QFrame
    entery_update_btn: QPushButton
    entery_delete_btn: QPushButton


class StudentFormUI:
    Form: QWidget
    frame_2: QFrame
    activity: QComboBox
    birthday: QDateEdit
    excused: QComboBox
    label_17: QLabel
    parent: QLineEdit
    label_18: QLabel
    gender: QComboBox
    label_7: QLabel
    note: QLineEdit
    label_11: QLabel
    label_16: QLabel
    label_9: QLabel
    date_inscrit: QDateEdit
    num_tel_2: QLineEdit
    label_12: QLabel
    name: QLineEdit
    num_tel: QLineEdit
    label_5: QLabel
    cin: QLineEdit
    label_6: QLabel
    label_2: QLabel
    label_3: QLabel


class TeacherFormUI:
    Form: QWidget
    frame_4: QFrame
    frame: QFrame
    name: QLineEdit
    label_2: QLabel
    frame_2: QFrame
    date_inscrit: QDateEdit
    label_4: QLabel
    frame_3: QFrame
    birthday: QDateEdit
    label_3: QLabel
    frame_5: QFrame
    phone: QLineEdit
    label_9: QLabel
    frame_6: QFrame
    phone_2: QLineEdit
    label_5: QLabel
    frame_8: QFrame
    note: QLineEdit
    label_6: QLabel


class RoleUI:
    role_form: QWidget
    frame: QFrame
    frame_5: QFrame
    reset_btn: QPushButton
    search_btn: QPushButton
    name_search: QComboBox
    label_19: QLabel
    frame_4: QFrame
    name: QLineEdit
    label_10: QLabel
    frame_2: QFrame
    frame_3: QFrame
    students: QCheckBox
    teachers: QCheckBox
    classes: QCheckBox
    payment: QCheckBox
    absents: QCheckBox
    money: QCheckBox
    settings: QCheckBox
    user: QCheckBox
    payment_edit: QCheckBox
    frame_6: QFrame
    delete_btn: QPushButton
    add_btn: QPushButton
    update_btn: QPushButton
    new_btn: QPushButton
    all_btn: QPushButton


class SettingsUI:
    teacher: QWidget
    frame: QFrame
    fr_btn: QPushButton
    payment_btn: QPushButton
    expense_btn: QPushButton
    income_btn: QPushButton
    way_btn: QPushButton
    plane: QStackedWidget
    stackedWidgetPage1: QWidget


class UserUI:
    users: QWidget
    frame_2: QFrame
    role: QComboBox
    label_14: QLabel
    passwd: QLineEdit
    label_5: QLabel
    user: QLineEdit
    label_10: QLabel
    frame: QFrame
    tbl: QTableWidget
    frame_3: QFrame
    delete_btn: QPushButton
    update_btn: QPushButton
    frame_5: QFrame
    add_btn: QPushButton
    new_btn: QPushButton


class UserPartUI:
    user_part: QWidget
    frame: QFrame
    add_role: QPushButton
    user: QPushButton
    stackedWidget: QStackedWidget


class AddPaymentUI:
    Form: QWidget
    frame_5: QFrame
    frame: QFrame
    frame_9: QFrame
    name: QLabel
    label_6: QLabel
    frame_7: QFrame
    classroom: QComboBox
    label_3: QLabel
    frame_12: QFrame
    way: QComboBox
    label_4: QLabel
    frame_15: QFrame
    bill_number: QLineEdit
    label_9: QLabel
    frame_14: QFrame
    cheq_num: QLineEdit
    label_8: QLabel
    frame_8: QFrame
    price: QDoubleSpinBox
    label_5: QLabel
    frame_34: QFrame
    addition_date: QDateEdit
    label_19: QLabel
    date: QDateEdit
    label_18: QLabel
    frame_10: QFrame
    confirm_btn: QPushButton
    reset_btn: QPushButton
    add_btn: QPushButton
    frame_6: QFrame
    bill_tbl: QTableWidget
    frame_4: QFrame
    search_student: QLineEdit
    student_list: QTableView


class PaymentPartUI:
    Form: QWidget
    frame: QFrame
    label: QLabel
    frame_3: QFrame
    view_not_payed: QPushButton
    view_payment: QPushButton
    stackedWidget: QStackedWidget


class ViewNotPayedUI:
    Form: QWidget
    tbl: QListWidget
    frame_35: QFrame
    frame_37: QFrame
    classroom: QComboBox
    label_21: QLabel
    frame_38: QFrame
    month: QSpinBox
    label_22: QLabel
    frame_39: QFrame
    year: QSpinBox
    label_23: QLabel
    frame_40: QFrame
    reset_btn: QPushButton
    search_btn: QPushButton


class ViewPaymentUI:
    view_payment: QWidget
    frame_33: QFrame
    stackedWidget: QStackedWidget
    page: QWidget
    label_17: QLabel
    frame: QFrame
    edit_btn: QPushButton
    delete_btn: QPushButton
    add_btn: QPushButton
    reg_tbl: QTableView
    frame_11: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    nb: QLabel
    label_19: QLabel
    total: QLabel
    label_20: QLabel
    page_2: QWidget
    label_18: QLabel
    frame_2: QFrame
    previous_price: QLabel
    label_22: QLabel
    frame_3: QFrame
    new_price: QDoubleSpinBox
    label_23: QLabel
    frame_34: QFrame
    cancel_btn: QPushButton
    update_btn: QPushButton
    search_frame: QFrame
    frame_28: QFrame
    search_ent: QLineEdit
    student_list: QListWidget
    frame_15: QFrame
    num_inscrit: QLineEdit
    label_9: QLabel
    frame_29: QFrame
    classroom: QComboBox
    label_14: QLabel
    frame_13: QFrame
    way: QComboBox
    label_7: QLabel
    frame_30: QFrame
    du: QDateEdit
    label_15: QLabel
    frame_31: QFrame
    to: QDateEdit
    label_16: QLabel
    frame_32: QFrame
    reset_btn: QPushButton
    search_btn: QPushButton


class StudentHistoryUI:
    student_history: QWidget
    frame: QFrame
    num_ins_search: QLineEdit
    label_11: QLabel
    student_tab: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton


class StudentPartUI:
    student_part: QWidget
    frame: QFrame
    classes_per_student: QPushButton
    students_history: QPushButton
    students: QPushButton
    stackedWidget: QStackedWidget


class StudentsUI:
    students: QWidget
    frame: QFrame
    frame_4: QFrame
    search_by_name: QLineEdit
    label_10: QLabel
    maximize: QPushButton
    frame_2: QFrame
    new_year: QPushButton
    new_btn: QPushButton
    delete_btn: QPushButton
    update_btn: QPushButton
    add_btn: QPushButton
    student_tab: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton
    search_frame: QFrame
    minimize: QPushButton
    groupBox_2: QGroupBox
    du: QDateEdit
    to: QDateEdit
    groupBox_3: QGroupBox
    excused_search: QComboBox
    groupBox_4: QGroupBox
    activity_search: QComboBox
    groupBox_6: QGroupBox
    gender_search: QComboBox
    groupBox_5: QGroupBox
    nb: QLabel


class TeacherUI:
    Form: QWidget
    frame_11: QFrame
    frame_12: QFrame
    nb: QLabel
    label_8: QLabel
    search: QLineEdit
    label_7: QLabel
    frame_7: QFrame
    new_year_btn: QPushButton
    update_btn: QPushButton
    delete_btn: QPushButton
    add_btn: QPushButton
    teachers_table: QTableView
    frame_13: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton


class TeacherHistoryUI:
    teacher_history: QWidget
    frame_2: QFrame
    nb: QLabel
    label_8: QLabel
    search: QLineEdit
    label_7: QLabel
    history_table: QTableView
    frame_7: QFrame
    printing_btn: QPushButton
    export_btn: QPushButton
    reset_btn: QPushButton
    search_btn: QPushButton


class TeacherPartUI:
    teacher_part: QWidget
    frame: QFrame
    teacher_history: QPushButton
    teacher: QPushButton
    stackedWidget: QStackedWidget
