CREATE DATABASE `pacer_case_details` CHARACTER SET utf8 COLLATE utf8_unicode_ci;

USE `pacer_case_details`;

CREATE TABLE IF NOT EXISTS `extractor_type` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`extractor_type_value` VARCHAR(55),
	PRIMARY KEY(`id`)
) ENGINE=INNODB;

INSERT INTO extractor_type(extractor_type_value) VALUES('DATE_RANGE');
INSERT INTO extractor_type(extractor_type_value) VALUES('REFRESH_CASE');
INSERT INTO extractor_type(extractor_type_value) VALUES('PACER_IMPORT_CASE');
INSERT INTO extractor_type(extractor_type_value) VALUES('PARSE_FILE');
INSERT INTO extractor_type(extractor_type_value) VALUES('FIND_CASE');

CREATE TABLE IF NOT EXISTS `extractor` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`extractor_type_id` INT,
	`is_local_parsing` TINYINT(1),
	`pacer_case_id` VARCHAR(55),
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
  PRIMARY KEY (`id`),
	FOREIGN KEY (`extractor_type_id`) REFERENCES extractor_type(`id`) ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `download_tracker` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`is_parsed`  TINYINT(1),
	`page_path`  VARCHAR(110),
  PRIMARY KEY (`id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `courtcase_source` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`value`  VARCHAR(55),
  PRIMARY KEY (`id`)
) ENGINE=INNODB;

INSERT INTO courtcase_source(value) VALUES('METADATA');
INSERT INTO courtcase_source(value) VALUES('DEFAULT');

CREATE TABLE IF NOT EXISTS  `courtcase` (
	`id` INT NOT NULL AUTO_INCREMENT,
  `download_tracker_id` INT NOT NULL,
	`courtcase_source_value` INT NOT NULL,
	`pacer_case_id` VARCHAR(55),
  `case_number` VARCHAR(55),
	`parties_involved` VARCHAR(255),
	`case_filed_date` DATE,
	`case_closed_date` DATE,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`download_tracker_id`) REFERENCES download_tracker(`id`) ON DELETE CASCADE,
	UNIQUE KEY courtcase_key (case_number, pacer_case_id),
	FOREIGN KEY (`courtcase_source_value`) REFERENCES courtcase_source(`id`) ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `courtcase_source_data_path` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`courtcase_id` INT,
	`page_value_json`  TEXT,
  FOREIGN KEY (`courtcase_id`) REFERENCES courtcase(`id`) ON DELETE CASCADE,
  PRIMARY KEY (`id`)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS  `additional_info` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`courtcase_id` INT,
	`additional_info_json` TEXT,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`courtcase_id`) REFERENCES courtcase(`id`) ON DELETE CASCADE
) ENGINE=INNODB;
