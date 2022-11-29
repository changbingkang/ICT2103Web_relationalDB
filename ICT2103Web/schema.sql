create table users( id integer AUTO_INCREMENT PRIMARY KEY, name text not null, password text not null, admin boolean not null DEFAULT '0');

create table emp (empid integer AUTO_INCREMENT PRIMARY KEY, name text not null, email text, phone integer, address text, joining_date timestamp DEFAULT CURRENT_TIMESTAMP, total_projects integer DEFAULT 1, total_test_case integer DEFAULT 1, total_defects_found integer DEFAULT 1, total_defects_pending integer DEFAULT 1);

CREATE TABLE "population" (
	"financial_year"	INTEGER NOT NULL,
	"town"	TEXT NOT NULL,
	"population"	INTEGER NOT NULL,
	PRIMARY KEY("town")
);

CREATE TABLE "pharmacy" (
	"id"	INTEGER,
	"town"	TEXT NOT NULL,
	"pharmacy_name"	TEXT NOT NULL,
	"incharge"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("town") REFERENCES "population"("town") ON DELETE CASCADE
);

CREATE TABLE "supermarkets" (
	"id"	INTEGER,
	"town"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"company_name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("town") REFERENCES "population"("town")  ON DELETE CASCADE
);

CREATE TABLE "rental" (
	"id"	INTEGER,
	"town"	TEXT NOT NULL,
	"rent_approve_date"	TEXT NOT NULL,
	"block"	TEXT NOT NULL,
	"street"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"monthly_rent"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("town") REFERENCES "population"("town")  ON DELETE CASCADE
);

CREATE TABLE "resaleflat" (
	"id"	INTEGER,
	"month"	TEXT NOT NULL,
	"town"	TEXT NOT NULL,
	"flat_type"	TEXT NOT NULL,
	"block"	TEXT NOT NULL,
	"street_name"	TEXT NOT NULL,
	"storey_range"	TEXT NOT NULL,
	"sq_size"	TEXT NOT NULL,
	"flat_model"	TEXT NOT NULL,
	"lease_commence_date"	TEXT NOT NULL,
	"resale_price"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("town") REFERENCES "population"("town") ON DELETE CASCADE
);

CREATE TABLE "school" (
	"name"	TEXT NOT NULL,
	"url_address"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"postal"	TEXT NOT NULL,
	"phone"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"mrt"	TEXT NOT NULL,
	"bus"	TEXT NOT NULL,
	"town"	TEXT NOT NULL,
	"zone"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"nature"	TEXT NOT NULL,
	"mainlvl"	TEXT NOT NULL,
	FOREIGN KEY("town") REFERENCES "population"("town")  ON DELETE CASCADE,
	PRIMARY KEY("name")
);

CREATE TABLE "subject" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"subject"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("name") REFERENCES "school"("name") ON DELETE CASCADE
);

CREATE TABLE "cca" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"cca_group"	TEXT NOT NULL,
	"cca_name"	TEXT NOT NULL,
	"special_name"	TEXT NOT NULL,
	FOREIGN KEY("name") REFERENCES "school"("name") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "users" (
	"id"	INTEGER,
	"name"	text NOT NULL,
	"password"	text NOT NULL,
	"admin"	boolean NOT NULL DEFAULT '0',
	PRIMARY KEY("id" AUTOINCREMENT)
);