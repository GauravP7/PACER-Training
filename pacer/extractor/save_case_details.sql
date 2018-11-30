CREATE DATABASE `pacer_case_details` CHARACTER SET utf8 COLLATE utf8_unicode_ci;

USE `pacer_case_details`;

CREATE TABLE IF NOT EXISTS `extractor` (
	`id` int NOT NULL AUTO_INCREMENT,
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
    	PRIMARY KEY (`id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `page_content` (
	`id` int NOT NULL AUTO_INCREMENT,
	`page_path`  VARCHAR(110),
    	PRIMARY KEY (`page_content_id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `page_source_path` (
	`id` int NOT NULL AUTO_INCREMENT,
	`case_details_id` int,
	`page_value_json`  TEXT,
    	FOREIGN KEY (`case_details_id`) REFERENCES case_details(`id`)
    	PRIMARY KEY (`id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `case_details` (
	`id` int NOT NULL AUTO_INCREMENT,
  `page_content_id` int NOT NULL,
  `case_number` VARCHAR(55),
	`parties_involved` VARCHAR(255),
	`case_filed_date` DATE,
	`case_closed_date` DATE,
    	PRIMARY KEY (`case_id`),
    	FOREIGN KEY (`page_content_id`) REFERENCES page_content(`id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `additional_info` (
	`id` int NOT NULL AUTO_INCREMENT,
	`case_details_id` int,
	`additional_info_json` TEXT,
    	PRIMARY KEY (`info_id`),
    	FOREIGN KEY (`case_details_id`) REFERENCES case_details(`id`)
) ENGINE=INNODB;
