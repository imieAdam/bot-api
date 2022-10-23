PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "visit_to_location" (
	"visit_to_location_id"	INTEGER,
	"visit_id"	INTEGER NOT NULL,
	"location_id"	INTEGER NOT NULL,
	PRIMARY KEY("visit_to_location_id")
);
INSERT INTO visit_to_location VALUES(1,1,5);
INSERT INTO visit_to_location VALUES(2,1,1);
INSERT INTO visit_to_location VALUES(3,1,2);
INSERT INTO visit_to_location VALUES(4,2,4);
INSERT INTO visit_to_location VALUES(5,3,1);
INSERT INTO visit_to_location VALUES(6,3,2);
INSERT INTO visit_to_location VALUES(7,4,5);
INSERT INTO visit_to_location VALUES(8,4,1);
INSERT INTO visit_to_location VALUES(9,4,2);
INSERT INTO visit_to_location VALUES(10,5,5);
INSERT INTO visit_to_location VALUES(11,5,3);
INSERT INTO visit_to_location VALUES(12,5,2);
CREATE TABLE IF NOT EXISTS "specializations" (
	"specialization_id"	INTEGER,
	"specialization"	TEXT NOT NULL,
	PRIMARY KEY("specialization_id")
);
INSERT INTO specializations VALUES(1,'Stomatolog');
INSERT INTO specializations VALUES(2,'Okulista');
INSERT INTO specializations VALUES(3,'Internista');
INSERT INTO specializations VALUES(4,'Ortopeda');
INSERT INTO specializations VALUES(5,'Endokrynolog');
CREATE TABLE IF NOT EXISTS "time_frames" (
	"time_frame_id"	INTEGER,
	"visit_id"	INTEGER NOT NULL,
	"start_time"	TEXT NOT NULL,
	"end_time"	TEXT NOT NULL,
	PRIMARY KEY("time_frame_id")
);
INSERT INTO time_frames VALUES(1,1,'08:00','09:30');
INSERT INTO time_frames VALUES(2,1,'15:30','22:00');
INSERT INTO time_frames VALUES(3,2,'07:00','10:00');
INSERT INTO time_frames VALUES(4,2,'15:00','22:00');
INSERT INTO time_frames VALUES(5,3,'09:00','11:00');
INSERT INTO time_frames VALUES(6,4,'08:11','09:31');
INSERT INTO time_frames VALUES(7,5,'08:11','09:01');
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER,
	"user_name"	TEXT NOT NULL UNIQUE,
	"user_password"	TEXT NOT NULL,
	PRIMARY KEY("user_id")
);
INSERT INTO users VALUES(1,'admin','admin');
INSERT INTO users VALUES(2,'admin2','admin2');
CREATE TABLE IF NOT EXISTS "user_portal_credentials" (
	"user_portal_credentials_id"	INTEGER,
	"login_email"	TEXT NOT NULL,
	"login_password"	TEXT NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"portal_name"	TEXT NOT NULL,
	PRIMARY KEY("user_portal_credentials_id")
);
CREATE TABLE IF NOT EXISTS "visits" (
	"visit_id"	INTEGER,
	"specialization_id"	INTEGER NOT NULL DEFAULT 0,
	"after_date"	TEXT,
	"booked_date_time"	TEXT,
	"booked_location"	INTEGER,
	"booked_doctor"	TEXT,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("visit_id")
);
INSERT INTO visits VALUES(1,2,'2020-10-01','2020-11-25T21:37:00.000',1,'Joe Doe',1);
INSERT INTO visits VALUES(2,5,'2020-10-01','2020-11-25T19:00:00.000',1,'Joe Doe',1);
INSERT INTO visits VALUES(3,4,'2020-10-10',NULL,NULL,NULL,1);
INSERT INTO visits VALUES(4,3,'2020-11-01',NULL,NULL,NULL,2);
INSERT INTO visits VALUES(5,1,'2020-11-01',NULL,NULL,NULL,2);
CREATE TABLE IF NOT EXISTS "locations" (
	"location_id"	INTEGER,
	"address"	TEXT NOT NULL,
	"city_id"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("location_id")
);
INSERT INTO locations VALUES(1,'ul. Opolska 110',1);
INSERT INTO locations VALUES(2,'ul. Jasnogórska 11',1);
INSERT INTO locations VALUES(3,'ul. Lublańska 38',1);
INSERT INTO locations VALUES(4,'al. Pokoju 5',1);
INSERT INTO locations VALUES(5,'ul. Wadowicka 7',1);
INSERT INTO locations VALUES(6,'ul. Starowiejska 189',2);
INSERT INTO locations VALUES(7,'ul. Krakowska 10',2);
CREATE TABLE IF NOT EXISTS "cities" (
	"city_id"	INTEGER,
	"name"	TEXT,
	PRIMARY KEY("city_id")
);
INSERT INTO cities VALUES(1,'Kraków');
INSERT INTO cities VALUES(2,'Radomsko');
COMMIT;
