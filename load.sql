CREATE DATABASE IF NOT EXISTS datarepresentation;
CREATE TABLE student (ID int auto_increment,Name varchar(255),Age int,PRIMARY KEY(ID));
CREATE TABLE lecturer (ID int auto_increment,Name varchar(255),Age int,PRIMARY KEY(ID));
INSERT INTO student (Name,Age) values("Alan Johnson",20);
INSERT INTO lecturer (Name,Age) values("John Smith",40);