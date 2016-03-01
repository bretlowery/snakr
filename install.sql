/*
DROP TABLE IF EXISTS `snakr_log_cli_ip_address`;
DROP TABLE IF EXISTS `snakr_log_cli_geo_city`;
DROP TABLE IF EXISTS `snakr_log_cli_geo_country`;
DROP TABLE IF EXISTS `snakr_log_cli_http_host`;
DROP TABLE IF EXISTS `snakr_log_cli_http_user_agent`;
DROP TABLE IF EXISTS `snakr_log_messages`;
DROP TABLE IF EXISTS `snakr_log`;
DROP TABLE IF EXISTS `snakr_shorturls`;
DROP TABLE IF EXISTS `snakr_longurls`;

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

*/

DROP TABLE IF EXISTS `snakr_eventlog`;
DROP TABLE IF EXISTS `snakr_eventlog_cli_ip_address`;
DROP TABLE IF EXISTS `snakr_eventlog_cli_geo_city`;
DROP TABLE IF EXISTS `snakr_eventlog_cli_geo_country`;
DROP TABLE IF EXISTS `snakr_eventlog_cli_http_host`;
DROP TABLE IF EXISTS `snakr_eventlog_cli_http_user_agent`;
DROP TABLE IF EXISTS `snakr_eventlog_messages`;

CREATE TABLE `snakr_eventlog` (
  `id` bigint(20) unsigned  NOT NULL AUTO_INCREMENT,
  `logged_on` datetime NOT NULL,
  `log_yyyymmddhh` integer unsigned NOT NULL,
  `entry_type` char(1) NOT NULL,
  `message_id` BIGINT unsigned NOT NULL,
  `longurl_id` bigint(20) unsigned NOT NULL,
  `shorturl_id` bigint(20) unsigned  NOT NULL,
  `cli_ip_address_id` bigint(20) unsigned  NOT NULL,
  `cli_geo_lat` decimal(10,8) unsigned  NOT NULL,
  `cli_geo_long` decimal(11,8) unsigned NOT NULL,
  `cli_geo_city_id` bigint(20) unsigned NOT NULL,
  `cli_geo_country_id` bigint(20) unsigned NOT NULL,
  `cli_http_host_id` bigint(20) unsigned NOT NULL,
  `cli_http_user_agent_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE UNIQUE INDEX `ui_exportkey` ON `snakr_eventlog`(`log_yyyymmddhh`, `entry_type`,`id`);
CREATE UNIQUE INDEX `ui_longurl_id` ON `snakr_eventlog`(`longurl_id`,`id`);
CREATE UNIQUE INDEX `ui_shorturl_id` ON `snakr_eventlog`(`shorturl_id`,`id`);
CREATE UNIQUE INDEX `ui_message_id` ON `snakr_eventlog`(`message_id`,`id`);
CREATE UNIQUE INDEX `ui_cli_ip_address_id` ON `snakr_eventlog`(`cli_ip_address_id`,`id`);
CREATE UNIQUE INDEX `ui_cli_geo_city_id` ON `snakr_eventlog`(`cli_geo_city_id`,`id`);
CREATE UNIQUE INDEX `ui_cli_geo_country_id` ON `snakr_eventlog`(`cli_geo_country_id`,`id`);
CREATE UNIQUE INDEX `ui_cli_http_host_id` ON `snakr_eventlog`(`cli_http_host_id`,`id`);
CREATE UNIQUE INDEX `ui_cli_http_user_agent_id` ON `snakr_eventlog`(`cli_http_user_agent_id`,`id`);


CREATE TABLE `snakr_eventlog_cli_ip_address` (
  `id` bigint(20) unsigned NOT NULL,
  `cli_ip_address` binary(128) NOT NULL,  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `snakr_eventlog_cli_ip_address` (
  `id` ,
  `cli_ip_address` 
)
VALUES (
	binary(0),
    'unknown'
);

CREATE TABLE `snakr_eventlog_cli_geo_city` (
  `id` bigint(20) unsigned NOT NULL,
  `cli_geo_city` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `snakr_eventlog_cli_geo_city` (
  `id` ,
  `cli_geo_city` 
)
VALUES (
	0,
    'unknown'
);

CREATE TABLE `snakr_eventlog_cli_geo_country` (
  `id` bigint(20) unsigned NOT NULL,
  `cli_geo_country` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `snakr_eventlog_cli_geo_country` (
  `id` ,
  `cli_geo_country` 
)
VALUES (
	0,
    'unknown'
);

CREATE TABLE `snakr_eventlog_cli_http_host` (
  `id` bigint(20) unsigned NOT NULL,
  `cli_http_host` varchar(253) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `snakr_eventlog_cli_http_host` (
  `id` ,
  `cli_http_host` 
)
VALUES (
	0,
    'unknown'
);

CREATE TABLE `snakr_eventlog_cli_http_user_agent` (
  `id` bigint unsigned NOT NULL,
  `cli_http_user_agent` VARCHAR(8192) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `snakr_eventlog_cli_http_user_agent` (
  `id` ,
  `cli_http_user_agent` 
)
VALUES (
	0,
    'unknown'
);

CREATE TABLE `snakr_eventlog_messages` (
  `log_id` bigint(20) unsigned NOT NULL,
  `message` VARCHAR(512) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `snakr_eventlog_messages` (
  `log_id` ,
  `message` 
)
VALUES (
	0,
    'none'
);