drop database if exists coffee;
create database coffee;
use coffee;

create table if not exists coworkers (
    cid INT PRIMARY KEY auto_increment,
    name VARCHAR(25),
    drink_preference VARCHAR(25),
    price decimal(5,2),
    debt decimal(10,2) DEFAULT 0.0
);

create table if not exists transactions(
	tid int primary key auto_increment,
    payer int,
    tdate date,
    amount decimal(5,2) not null,
	foreign key (payer) references coworkers(cid) on delete cascade
);

create table if not exists payment(
	pid int primary key auto_increment,
    payer int not null,
    payee int not null,
    amount decimal(5,2),
    tid int,
    foreign key (payer) references coworkers(cid) on delete cascade,
    foreign key (payee) references coworkers(cid)on delete cascade,
    foreign key (tid) references transactions(tid)on delete cascade);

insert into coworkers values (1,"Bob","Latte",3.50,0);
insert into coworkers values (2,"Jeremy","Americano",4,0);
insert into coworkers values (3,"Alex","Coffee",2,0);
insert into coworkers values (4,"Harika","Chai",2.50,0);
insert into coworkers values (5,"Amy","Black Tea",3.75,0);
insert into coworkers values (6,"Ben","Caramel Latte",2.20,0);
insert into coworkers values (7,"Alice","Peppermint Tea",3,0);

select * from payment;