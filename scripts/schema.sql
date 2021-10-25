DROP TABLE IF EXISTS Task;


create table if not exists Task
(
    id              int auto_increment  primary key,
    parameters      varchar(32)                        not null,
    result          varchar(32)                        not null,
    worker_name     varchar(32)                        not null,
    state           varchar(8)                         not null,
    start           datetime                           not null,
    end             datetime                           not null
);
