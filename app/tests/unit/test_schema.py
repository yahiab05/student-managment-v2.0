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
        "rep": "rep",
        "date_rep": "2022-01-01"
    }