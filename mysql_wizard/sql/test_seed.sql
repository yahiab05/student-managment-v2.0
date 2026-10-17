USE `legacy_db`;

INSERT INTO `settings` (`name`) VALUES ('CI Test Teaching Way');

INSERT INTO `teacher` (`name`, `id`, `phone`, `birthday`, `note`, `date_inscrit`, `user`)
VALUES ('CI Test Teacher', 990001, '00000000', '1990-01-01', 'CI fixture', '2026-01-01', 'ci');

INSERT INTO `students` (
    `name`, `gender`, `birthday`, `num_inscrit`, `date_inscrit`, `parent`,
    `cin`, `activite`, `num_tel`, `excused`, `class`, `note`, `user`
)
VALUES (
    'CI Test Student', 'M', '2015-01-01', 990001, '2026-01-01', 'CI Parent',
    '990001', 'active', '00000000', 'no', 'CI Test Class', 'CI fixture', 'ci'
);

INSERT INTO `classes` (`name`, `way`, `teacher`, `note`, `price`, `user`)
VALUES ('CI Test Class', 'CI Test Teaching Way', 'CI Test Teacher', 'CI fixture', 10, 'ci');

INSERT INTO `classeleve` (`student`, `class`, `birthday`, `num_inscrit`, `excused`, `date`, `user`, `phone`)
VALUES ('CI Test Student', 'CI Test Class', '2015-01-01', '990001', 'no', '2026-01-01', 'ci', '00000000');

INSERT INTO `users` (`id`, `username`, `password`, `role`)
VALUES (990001, 'ci_test_user', 'ci_test_password', 'programmer');