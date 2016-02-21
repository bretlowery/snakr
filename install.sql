CREATE TABLE `snakr_longurls` (
  `id` bigint(20) NOT NULL,
  `longurl` varchar(4096) NOT NULL,
  `created_on` datetime NOT NULL,
  `originally_encoded` char(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `snakr_shorturls` (
  `id` bigint(20) NOT NULL,
  `longurl_id` bigint(20) NOT NULL,
  `shorturl` varchar(40) NOT NULL,
  `shorturl_path_size` smallint(6) NOT NULL,
  `created_on` datetime NOT NULL,
  `is_active` char(1) NOT NULL,
  `compression_ratio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `longurl_id` (`longurl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `snakr_log` (
  `log_order` bigint(20) NOT NULL AUTO_INCREMENT,
  `logged_on` datetime NOT NULL,
  `entry_type` char(1) NOT NULL,
  `longurl_id` bigint(20) NOT NULL,
  `shorturl_id` bigint(20) NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `lat` decimal(10,8) NOT NULL,
  `long` decimal(11,8) NOT NULL,
  `city_of_origin` varchar(100) NOT NULL,
  `country_of_origin` varchar(100) NOT NULL,
  PRIMARY KEY (`log_order`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

ALTER TABLE `snakr_log` CHANGE  `ip_address` `cli_ip_address` VARCHAR(255) NOT NULL;
ALTER TABLE `snakr_log` CHANGE  `lat` `cli_geo_lat` decimal(10,8) NOT NULL;
ALTER TABLE `snakr_log` CHANGE  `long` `cli_geo_long` decimal(11,8) NOT NULL;
ALTER TABLE `snakr_log` CHANGE  `city_of_origin` `cli_geo_city` varchar(100) NOT NULL;
ALTER TABLE `snakr_log` CHANGE  `country_of_origin` `cli_geo_country` varchar(100) NOT NULL;
ALTER TABLE `snakr_log` ADD `cli_http_host` varchar(128) NOT NULL;
ALTER TABLE `snakr_log` ADD `cli_http_referrer` varchar(2048) NOT NULL;
ALTER TABLE `snakr_log` ADD `cli_http_user_agent` varchar(8192) NOT NULL;

ALTER TABLE `snakr_log` ADD `cli_http_host_hash` BIGINT NOT NULL;
ALTER TABLE `snakr_log` ADD `cli_http_referrer_hash` BIGINT NOT NULL;
ALTER TABLE `snakr_log` ADD `cli_http_user_agent_hash` BIGINT NOT NULL;






