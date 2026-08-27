from datetime import date as DateType
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from PyQt6.QtCore import QDate
from app.repo.database import Base

class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    classes: Mapped[bool] = mapped_column( nullable=False)
    students: Mapped[bool] = mapped_column( nullable=False)
    teachers: Mapped[bool] = mapped_column( nullable=False)
    payment: Mapped[bool] = mapped_column( nullable=False)
    money: Mapped[bool] = mapped_column( nullable=False)
    settings: Mapped[bool] = mapped_column( nullable=False)
    user: Mapped[bool] = mapped_column( nullable=False)
    payment_editting: Mapped[bool] = mapped_column( nullable=False)


    def __repr__(self):
        return f"Role(id={self.id}, name={self.name}, classes={self.classes}, students={self.students}, teachers={self.teachers})"


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role_name: Mapped[Optional[str]] = mapped_column(String(255), ForeignKey("role.name"))

    role: Mapped[Optional["Role"]] = relationship("Role", backref="users", lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, password={self.password})"
    

class Students(Base):
    __tablename__ = "students"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[str] = mapped_column(String(255), nullable=False)
    birthday: Mapped[DateType] = mapped_column(nullable=False)
    date_inscrit: Mapped[DateType] = mapped_column(nullable=False)
    parent: Mapped[str] = mapped_column(String(255), nullable=False)
    cin: Mapped[int] = mapped_column(nullable=False)
    activity: Mapped[str] = mapped_column(String(255), nullable=False)
    num_tel: Mapped[str] = mapped_column(String(255), nullable=False)
    excused: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[str] = mapped_column(String(255), nullable=False)
    user: Mapped[str] = mapped_column(String(255), nullable=False)

    courses: Mapped[list["Classes"]] = relationship("Classes", secondary='classeleve', back_populates="students")

    def __repr__(self):
        return f"Student {self.id}"
    
    def set_birthday(self, date: QDate):
        return date.toPyDate()

    def get_birthday(self):
        return QDate.fromString(str(self.birthday), "yyyy-MM-dd")
    
    def set_date_inscrit(self, date: QDate):
        return date.toPyDate()

    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")
    
class StudentsHistory(Base):
    __tablename__ = "students_history"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    num_inscrit: Mapped[Optional[int]] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    date_inscrit: Mapped[DateType] = mapped_column(nullable=False)
    user: Mapped[str] = mapped_column(String(255), nullable=False)

    def set_date_inscrit(self, date: QDate):
        return date.toPyDate()

    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")

    student: Mapped["Students"] = relationship("Students", backref="students_history")
    

class Classes(Base):
    __tablename__ = "classes"
    __table_args__ = {"extend_existing": True}


    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    way: Mapped[str] = mapped_column(String(255), nullable=False)
    teacher: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    user: Mapped[str] = mapped_column(String(255), nullable=False)

    students: Mapped[list["Students"]] = relationship("Students", secondary="classeleve", back_populates="courses")

    def __repr__(self):
        return f"Class(id={self.id}, name={self.name}, way={self.way}, teacher={self.teacher}, price={self.price})"
    
class Teachers(Base):
    __tablename__ = "teachers"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    date_inscrit: Mapped[DateType] = mapped_column(nullable=False)
    birthday: Mapped[DateType] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[str] = mapped_column(String(255), nullable=False)
    user: Mapped[str] = mapped_column(String(255), nullable=False)

    def set_birthday(self, date: QDate):
        return date.toPyDate()

    def get_birthday(self):
        return QDate.fromString(str(self.birthday), "yyyy-MM-dd")
    
    def set_date_iscrit(self, date: QDate):
        return date.toPyDate()

    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")
    
class TeachersHistory(Base):
    __tablename__ = "teachershistory"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="SET NULL"))
    date_inscrit: Mapped[DateType] = mapped_column(nullable=False)
    user: Mapped[str] = mapped_column(String(255), nullable=False)

    def set_date_inscrit(self, date: QDate):
        return date.toPyDate()
    
    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")

    teacher: Mapped["Teachers"] = relationship("Teachers", backref="teachershistory")
    
class ClassEleve(Base):
    __tablename__ = "classeleve"
    __table_args__ = {"extend_existing": True}
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[Optional[int]] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    class_name: Mapped[Optional[str]] = mapped_column(String(255), ForeignKey("classes.name"))
    user: Mapped[str] = mapped_column(String(255), nullable=False)
    
    students: Mapped["Students"] = relationship("Students", backref="classeleve", lazy=True, viewonly=True)


class Settings(Base):
    __tablename__ = "settings"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    way_teaching: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    entery: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    entery_code: Mapped[Optional[int]] = mapped_column(unique=True)
    out_money: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    out_code: Mapped[Optional[int]] = mapped_column(unique=True)
    way_payment: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    fr: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    user: Mapped[str] = mapped_column(String(255), nullable=False)


class OutMoney(Base):
    __tablename__ = "outmoney"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    bill_number: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[DateType] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    way: Mapped[str] = mapped_column(String(255), nullable=False)
    cheq_num: Mapped[Optional[str]] = mapped_column(String(255))
    note: Mapped[str] = mapped_column(String(255),  nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    user: Mapped[str] = mapped_column(String(255), nullable=False)
    in_bank: Mapped[bool] = mapped_column(nullable=False)

    def __repr__(self):
        return f"OutMoney(id={self.id}, name={self.name}, bill_num={self.bill_num}, date={self.date}, price={self.price})"
    
    def set_date(self, date: QDate):
        return date.toPyDate()

    def get_date(self):
        return QDate.fromString(self.date.strftime("%Y-%m-%d"), "yyyy-MM-dd")
    
class Entery(Base):
    __tablename__ = "entery"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    num_inscrit: Mapped[Optional[int]] = mapped_column()
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    bill_number: Mapped[str] = mapped_column(String(255), nullable=False)
    payment_date: Mapped[Optional[DateType]] = mapped_column()
    addition_date: Mapped[DateType] = mapped_column(nullable=False)
    way: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    note: Mapped[Optional[str]] = mapped_column(String(255))
    user: Mapped[str] = mapped_column(String(255), nullable=False)
    cheq_num: Mapped[Optional[str]] = mapped_column(String(255))
    classroom: Mapped[Optional[str]] = mapped_column(String(255))
    in_bank: Mapped[bool] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Entery(id={self.id}, date={self.addition_date}, type={self.type}, code={self.code}, price={self.price})"
    
    def set_add_date(self, date: QDate):
        return date.toPyDate()

    def get_add_date(self):
        return QDate.fromString(self.addition_date.strftime("%Y-%m-%d"), "yyyy-MM-dd")
    
    def set_payment_date(self, date: QDate):
        return date.toPyDate()

    def get_payment_date(self):
        return QDate.fromString(self.payment_date.strftime("%Y-%m"), "yyyy-MM")


class Transfer(Base):
    __tablename__ = "transfer"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    price: Mapped[float] = mapped_column(nullable=False)
    origin: Mapped[str] = mapped_column(String(255), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[DateType] = mapped_column(nullable=False)
    note: Mapped[str] = mapped_column(String(255))
    user: Mapped[str] = mapped_column(String(255), nullable=False)