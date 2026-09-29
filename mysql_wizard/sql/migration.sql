SET autocommit = 1;
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_SAFE_UPDATES = 0;
SET GLOBAL wait_timeout = 28800;
SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;

-- auto increment reset
-- ---------------------------
-- settings
truncate table darcoran.settings;
ALTER TABLE darcoran.settings AUTO_INCREMENT = 1;

insert into darcoran.settings (
	entery_code, entery,
    out_money, out_code,
    way_payment, fr
    )
select 
	entery_code, entery,
    out_money, out_code,
    way_payment, fr
from {{old_db}}.settings_money;

insert into darcoran.settings (
	way_teaching
    )
select 
	`name`
from {{old_db}}.settings;

-- ---------------------
-- students
truncate table darcoran.students;

insert into darcoran.students (
	id, `name`, gender, birthday, activity,
    cin, parent, date_inscrit, num_tel, excused, note, `user`
    )
select
	num_inscrit, `name`, gender, 
    cast(birthday as date), 
    activite,
    cast(cin as signed), 
    parent, 
    cast(date_inscrit as date), 
    num_tel, excused, 
    coalesce(note, "") as note, 
    coalesce(`user`, "") as `user`
from {{old_db}}.students;
-- -----------------------------
-- teachers
truncate table darcoran.teachers;
ALTER TABLE darcoran.teachers AUTO_INCREMENT = 1;

insert into darcoran.teachers (
	`name`, 
    date_inscrit,
    birthday,
    phone,
    note,
    payed,
    `user`
    )
select 
	`name`,
	cast(date_inscrit as date),
    coalesce(
    cast(birthday as date),
    cast("2020-01-01" as date)
    ),
    coalesce(phone, ""),
    coalesce(note, ""),
    coalesce(money, ""),
    coalesce(`user`, "") as `user`
from {{old_db}}.teacher;
-- -----------------
-- students history
truncate table darcoran.students_history;
ALTER TABLE darcoran.students_history AUTO_INCREMENT = 1;

insert into darcoran.students_history(
	num_inscrit,
    date_inscrit,
    `user`
	)
select 
	num_inscrit,
	coalesce(
    cast(date_inscrit as date),
    cast("2020-01-01" as date)
    ),
    coalesce(`user`, "") as `user`
from {{old_db}}.students_history;
-- ----------------------
-- role
truncate table darcoran.`role`;
ALTER TABLE darcoran.`role` AUTO_INCREMENT = 1;

insert into darcoran.`role` (
	`name`, classes, students, teachers, payment, money, absent, settings, `user`, payment_editting
)
select 
	`name`,
    case
		when `class` = "" then 0
        else 1
	end as `class`,
    case
		when students = "" then 0
        else 1
	end as students,
    case
		when teacher = "" then 0
        else 1
	end as teacher,
    case
		when payment = "" then 0
        else 1
	end as payment,
    case
		when money = "" then 0
        else 1
	end as money,
    case
		when absent = "" then 0
        else 1
	end as absent,
    case
		when settings = "" then 0
        else 1
	end as settings,
    case
		when `user` = "" then 0
        else 1
	end as `user`,
    0 as payment_editting
from {{old_db}}.`role`;
-- -----------------------------
-- users
truncate table darcoran.users;
ALTER TABLE darcoran.users AUTO_INCREMENT = 1;

insert into darcoran.users (
	username, `password`, role_name
	)
select 
	username, `password`, `role`
from {{old_db}}.users;
-- -----------------------
-- classes
truncate table darcoran.classes;
ALTER TABLE darcoran.classes AUTO_INCREMENT = 1;

insert into darcoran.classes (
	`name`, way, teacher, note, price, `user`, seance, `exchange`, teacher_part
    )
select 
	`name`, way, teacher, note, 
    cast(price as decimal(10, 2)), 
    coalesce(`user`, "") as `user`, 
    coalesce(seance, 0), 
    coalesce(`exchange`, 0), 
    coalesce(cast(teacher_part as decimal(10, 2)), 0)
from {{old_db}}.classes;
-- ------------------------------
-- classelve
truncate table darcoran.classeleve;
ALTER TABLE darcoran.classeleve AUTO_INCREMENT = 1;

insert into darcoran.classeleve (
	student_id, class_name
    )
select
	num_inscrit, `class`
from {{old_db}}.classeleve;
