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
  `log_order` int(11) NOT NULL AUTO_INCREMENT,
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
