CREATE DATABASE event_database;

SHOW DATABASES;

USE event_database;

CREATE TABLE registrations (
    roll varchar(20) PRIMARY KEY,
    fullname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phno VARCHAR(15) NOT NULL,
    stream varchar(10) not null,
    event VARCHAR(20) NOT NULL
);

show tables;

DESCRIBE registrations;

select * from registrations;

delete from registrations where roll = 1;

drop database event_database;
