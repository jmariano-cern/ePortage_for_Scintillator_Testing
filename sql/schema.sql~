create table Card
(
	sn int not null,
	card_id int unsigned auto_increment,
	primary key (card_id),
	UNIQUE(sn)
);

create table Test_Type
(	
	test_type int unsigned auto_increment,
	primary key (test_type),
	name varchar(50),
	required tinyint(1) not null,
	desc_short varchar(100),
	desc_long varchar(1000),
	relative_order int not null,
	has_num_val tinyint(1) not null,
        val_names varchar(100),
        val_units varchar(100)
);

create table Test
(
	test_id int unsigned auto_increment,
	primary key (test_id),
	test_type_id int not null,
	card_id int not null,
	person_id int not null,
	day timestamp not null, 
	successful tinyint(1) not null,
	comments varchar(1000),
	INDEX (card_id),
	INDEX (person_id),
        vals varchar(1000)
); 	

create table People
(
	person_id int unsigned auto_increment,
	primary key (person_id),
	person_name varchar (100)
);

create table Attachments
(
	attach_id int unsigned auto_increment,	
	primary key (attach_id),
	test_id int,
	attachmime varchar (30),
	attachdesc varchar (1000),
	comments varchar (200),
	originalname varchar (200),
	INDEX (test_id)
);

create table Card_Info_Types
(
	info_type_id int unsigned auto_increment,
	primary key (info_type_id),
	Info_Name varchar (50),
	Info_Desc_Short varchar (100),
	Info_Desc_Long varchar (1000)
);

create table Card_Info
(
	info_id int unsigned auto_increment,
	primary key (info_id),
	card_id int not null,
	info_type int not null,
	info varchar (300),
	INDEX(card_id),
	INDEX(info_type)
);

create table TestRevoke
(
	test_id int unsigned not null,
	primary key(test_id),
	comment varchar(1000)
);
