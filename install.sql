DROP TABLE IF EXISTS `snakr_useragents`;
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

CREATE TABLE `snakr_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `logged_on` datetime NOT NULL,
  `entry_type` char(1) NOT NULL,
  `longurl_id` bigint(20) NOT NULL,
  `shorturl_id` bigint(20) NOT NULL,
  `cli_ip_address` binary(128) NOT NULL,
  `cli_geo_lat` decimal(10,8) NOT NULL,
  `cli_geo_long` decimal(11,8) NOT NULL,
  `cli_geo_city` varchar(100) NOT NULL,
  `cli_geo_country` varchar(100) NOT NULL,
  `cli_http_host` varchar(128) NOT NULL,
  `cli_http_user_agent_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;


CREATE TABLE `snakr_useragents` (
  `id` bigint NOT NULL,
  `cli_http_user_agent` VARCHAR(8192) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

