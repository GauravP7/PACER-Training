CREATE DATABASE `pacer_case_details` CHARACTER SET utf8 COLLATE utf8_unicode_ci;

USE `pacer_case_details`;

CREATE TABLE IF NOT EXISTS `extractor` (
	`extractor_id` int NOT NULL AUTO_INCREMENT,
`case_number`  VARCHAR(55),
`case_status`  VARCHAR(55),
`from_field_date`  DATE,
`to_field_date`  DATE,
`from_last_entry_date`  DATE,
`to_last_entry_date`  DATE,
`nature_of_suit`   VARCHAR(55),
`cause_of_action`   VARCHAR(55),
`last_name`  VARCHAR(55),
`first_name`  VARCHAR(55),
`middle_name`  VARCHAR(55),
`type`  VARCHAR(55),
`exact_matches_only`  TINYINT(1),
	PRIMARY KEY (`extractor_id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `page_content` (
	`page_content_id` int NOT NULL AUTO_INCREMENT,
	`page_path`  VARCHAR(110),
	PRIMARY KEY (`page_content_id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `case_details` (
	`case_id` int NOT NULL AUTO_INCREMENT,
  `page_content_id` int NOT NULL,
  `case_number` VARCHAR(55),
	`parties_involved` VARCHAR(255),
	`case_filed_date` DATE,
	`case_closed_date` DATE,
    	PRIMARY KEY (`case_id`),
    	FOREIGN KEY (`page_content_id`) REFERENCES
page_content(`page_content_id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `additional_info` (
	`info_id` int NOT NULL AUTO_INCREMENT,
	`case_id` int,
	`additional_info_json` TEXT,
    	PRIMARY KEY (`info_id`),
    	FOREIGN KEY (`case_id`) REFERENCES case_details(`case_id`)
) ENGINE=INNODB;

/*INSERT statements*/
/*
INSERT INTO extractor(case_number, case_status, from_field_date, to_field_date, from_last_entry_date, to_last_entry_date,
nature_of_suit, cause_of_action, last_name, first_name, middle_name, type, exact_matches_only)
VALUES('', '', '2007-1-1', '2008-1-1', NULL, NULL, '', '', '', '', '', '', 0);

INSERT INTO page_content(page_path) VALUES('/home/pacer_training');

INSERT INTO case_details(page_content_id, case_number, parties_involved, case_filed_date, case_closed_date)
VALUES(1, 'Case-123', 'ABC v. XYZ', '2007-10-01', '2009-01-01');

INSERT INTO additional_info(case_id, additional_info_json)
VALUES(1, "{'attorney':'https://case_attorney.com', 'mobile query':'https://case_mobile_query.com'}");
*/
