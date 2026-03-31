from app.repo.schemas import SchemaFactory
from app.repo.schemas import (
    AbsentSSchema,
    AbsentTSchema,
    ClassesSchema,
    EnrollmentSchema,
    StudentSchema,
    TeacherSchema,
    StudentHistorySchema,
    TeacherHistorySchema,
    EntrySchema,
    ExpensesSchema,
    StorageSchema,
    RoleSchema,
    SettingsSchema,
    UserSchema,
)
import pytest

    @pytest.mark.parametrize("schema_factory_member, expected_schema", [
        (SchemaFactory.ABSENT_S, AbsentSSchema),
        (SchemaFactory.ABSENT_T, AbsentTSchema),
        (SchemaFactory.CLASSES, ClassesSchema),
        (SchemaFactory.ENROLLMENT, EnrollmentSchema),
        (SchemaFactory.STUDENT, StudentSchema),
        (SchemaFactory.TEACHER, TeacherSchema),
        (SchemaFactory.STUDENT_HISTORY, StudentHistorySchema),
        (SchemaFactory.TEACHER_HISTORY, TeacherHistorySchema),
        (SchemaFactory.INCOME, EntrySchema),
        (SchemaFactory.EXPENSES, ExpensesSchema),
        (SchemaFactory.STORAGE, StorageSchema),
        (SchemaFactory.ROLE, RoleSchema),
        (SchemaFactory.SETTINGS, SettingsSchema),
        (SchemaFactory.USER, UserSchema)
        ])
    def test_schema_class_function(schema_factory_member, expected_schema):
        assert schema_factory_member.value == expected_schema
    
def test_create_function_absent_s():
    schema = SchemaFactory.ABSENT_S
    schema.create(
        num_inscrit=1,
        class_ab="A",
        date_ab="2022-01-01",
        du="00:00",
        time_last="00:00",
        user="user"
    )
    
    assert schema.to_dict() == {
        "num_inscrit": 1,
        "class_ab": "A",
        "date_ab": "2022-01-01",
        "du": "00:00",
        "time_last": "00:00",
        "user": "user"
    }
    
def test_create_function_absent_t():
    schema = SchemaFactory.ABSENT_T
    schema.create(
        num_inscrit=1,
        class_ab="A",
        date_ab="2022-01-01",
        du="00:00",
        time_last="00:00",
        user="user"
    )
    
<<<<<<< HEAD
    assert schema.to_dict() == {
=======
    assert schema.schema_class().to_dict() == {
>>>>>>> b939638 (unit tests first commit)
        "num_inscrit": 1,
        "class_ab": "A",
        "date_ab": "2022-01-01",
        "du": "00:00",
        "time_last": "00:00",
        "user": "user"
    }
    
    schema = SchemaFactory.ABSENT_T
    schema.create(
        num_inscrit=1,
        class_ab="A",
        date_ab="2022-01-01",
        du="00:00",
        time_last="00:00",
        user="user",
        rep="rep",
        date_rep="2022-01-01"
    )
    
<<<<<<< HEAD
    assert schema.to_dict() == {
=======
    assert schema.schema_class().to_dict() == {
>>>>>>> b939638 (unit tests first commit)
        "num_inscrit": 1,
        "class_ab": "A",
        "date_ab": "2022-01-01",
        "du": "00:00",
        "time_last": "00:00",
        "user": "user",
    }, None, None),
    (SchemaFactory.ABSENT_T, {
        "num_inscrit": 1,
        "class_ab": "A",
        "date_ab": "2022-01-01",
        "du": "00:00",
        "time_last": "00:00",
        "user": "user",
    }, 
    {
        "rep": "test",
        "date_rep": None
    },
    {
        "rep": "",
        "date_rep": None
    }),
    (SchemaFactory.CLASSES, {
        "name": "test",
        "way": "test",
        "teacher": "test",
        "note": "test",
        "price": 1.55,
        "seance": 1,
        "exchange": "test",
        "teacher_part": 1.55,
        "user": "user"
    }, None, None),
    (SchemaFactory.ENROLLMENT, {
        "student_id": 1,
        "class_name": "test",
        "user": "user"
    }, None, None),
    (SchemaFactory.STUDENT, {
        "num_inscrit": 1,
        "name": "test",
        "birthday": "2022-01-01",
        "parent": "test",
        "num_tel": "test",
        "date_inscrit": "2022-01-01",
        "cin": 1254668,
        "activity": "test",
        "excused": "test",
        "user"  : "user",
        "gender": "male"
    }, 
    {
        "note": ""
    }, 
    {
        "note": "test"
    }),
    (SchemaFactory.TEACHER,
    {
        "name": "Ali",
        "birthday": "2022-01-01",
        "date_inscrit": "2022-01-01",
        "phone": "20020014",
        "payed": "test",
        "user": "user"
    },
    {
        "note": ""
    },
    {   
        "note": "test"
    }),
    (SchemaFactory.STUDENT_HISTORY, {
        "num_inscrit": 1,
        "date_inscrit": "2022-01-01",
        "user": "user"
    }, None, None),
    (SchemaFactory.TEACHER_HISTORY, {
        "teacher_id": 1,
        "payed": "test",
        "user": "user",
        "date_inscrit": "2022-01-01"
    }, None, None),
    (SchemaFactory.INCOME, {
        "name": "Ali",
        "price": 100.52,
        "code": 13,
        "user": "user",
        "way": "way1",
        "type": "type1",
        "bill_number": "12548dd",

    }, 
    {
        "cheq_num": ""  ,
        "note": "",
        "num_inscrit": None,
        "payment_date": None,
        "addition_date": None,
        "classroom": None
    },
    {
        "cheq_num": "test",
        "note": "test",
        "num_inscrit": 1,
        "payment_date": "2022-01-01",
        "addition_date": "2022-01-01",
        "classroom": "test"
    }),
    (SchemaFactory.EXPENSES, {
        "name": "Ali",
        "price": 100.52,
        "code": 13,
        "user": "user",
        "way": "way1",
        "type": "type1",
        "bill_num": "12548dd",
        "date": "2022-01-01"
    }, 
    {
        "cheq_num": ""  ,
        "note": ""
    },
    {
        "cheq_num": "test",
        "note": "test"
    }),
    (SchemaFactory.STORAGE, {
        "income_id":1,
        "user": "user",
        "income": 100.52,
        "date": "2022-01-01",
    },
    {
        "expense_id": None,
        "expense": None,
        "note": ""
    },
    {
        "expense_id": None,
        "expense": None,
        "note": "test"
    }),
    (SchemaFactory.STORAGE, {
        "expense_id":1,
        "user": "user",
        "expense": 100.52,
        "date": "2022-01-01",
    },
    {
        "income_id": None,
        "income": None,
        "note": ""
    },
    {
        "income_id": None,
        "income": None,
        "note": "test"
    }),
    (SchemaFactory.ROLE, {
        "name": "test",
        "classes": True,
        "students": True,
        "teachers": True,
        "payment": True,
        "money": True,
        "absent": True,
        "settings": True,
        "user": True,
        "payment_editting": True
    }, None, None),
    (SchemaFactory.SETTINGS, {
        "way_teaching": "test",
        "entery": "test",
        "entery_code": 1,
        "out_money": "test",
        "out_code": 1,
        "way_payment": "test",
        "fr": "test"
    }, None, None),
    (SchemaFactory.USER, {
        "username": "test",
        "password": "test",
        "role_name": "test"
    }, None, None),
    (SchemaFactory.SETTINGS, {
        "way_teaching": "test",
        "entery": "test",
        "entery_code": 1,
        "out_money": "test",
        "out_code": 1,
        "way_payment": "test",
    }, None, {
        "fr": None
    })
])
def test_create_function(schema_factory_member, expected_schema, optional_args=None, default_args=None):
    if optional_args is not None:
        schema_factory_member.create(**expected_schema)
        output = expected_schema | optional_args
        
        assert schema_factory_member.schema_class().to_dict() == output
    
    if default_args is not None and optional_args is None:
        expected_schema = expected_schema | default_args
        schema_factory_member.create(**expected_schema)
        
        assert schema_factory_member.schema_class().to_dict() == expected_schema
    
    if default_args is None and optional_args is not None:
        expected_schema = expected_schema | default_args
        schema_factory_member.create(**expected_schema)
        
        assert schema_factory_member.schema_class().to_dict() == expected_schema
    
    
    
    
