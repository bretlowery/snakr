CREATE DATABASE  IF NOT EXISTS `snakr` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `snakr`;
-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- ------------------------------------------------------
-- Server version	5.6.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--
-- ORDER BY:  `id`

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add site',4,'add_site'),(11,'Can change site',4,'change_site'),(12,'Can delete site',4,'delete_site'),(13,'Can add log entry',5,'add_logentry'),(14,'Can change log entry',5,'change_logentry'),(15,'Can delete log entry',5,'delete_logentry'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add long ur ls',8,'add_longurls'),(23,'Can change long ur ls',8,'change_longurls'),(24,'Can delete long ur ls',8,'delete_longurls'),(25,'Can add short ur ls',9,'add_shorturls'),(26,'Can change short ur ls',9,'change_shorturls'),(27,'Can delete short ur ls',9,'delete_shorturls'),(28,'Can add event log',10,'add_eventlog'),(29,'Can change event log',10,'change_eventlog'),(30,'Can delete event log',10,'delete_eventlog'),(31,'Can add user agent log',11,'add_useragentlog'),(32,'Can change user agent log',11,'change_useragentlog'),(33,'Can delete user agent log',11,'delete_useragentlog'),(34,'Can add host log',12,'add_hostlog'),(35,'Can change host log',12,'change_hostlog'),(36,'Can delete host log',12,'delete_hostlog'),(37,'Can add city log',13,'add_citylog'),(38,'Can change city log',13,'change_citylog'),(39,'Can delete city log',13,'delete_citylog'),(40,'Can add country log',14,'add_countrylog'),(41,'Can change country log',14,'change_countrylog'),(42,'Can delete country log',14,'delete_countrylog'),(43,'Can add ip log',15,'add_iplog'),(44,'Can change ip log',15,'change_iplog'),(45,'Can delete ip log',15,'delete_iplog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--
-- ORDER BY:  `id`

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'auth','permission'),(2,'auth','group'),(3,'auth','user'),(4,'sites','site'),(5,'admin','logentry'),(6,'contenttypes','contenttype'),(7,'sessions','session'),(8,'snakr','longurls'),(9,'snakr','shorturls'),(10,'snakr','eventlog'),(11,'snakr','useragentlog'),(12,'snakr','hostlog'),(13,'snakr','citylog'),(14,'snakr','countrylog'),(15,'snakr','iplog');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `snakr_citylog`
--

DROP TABLE IF EXISTS `snakr_citylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snakr_citylog` (
  `id` bigint(20) NOT NULL,
  `city` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `snakr_citylog`
--
-- ORDER BY:  `id`

LOCK TABLES `snakr_citylog` WRITE;
/*!40000 ALTER TABLE `snakr_citylog` DISABLE KEYS */;
INSERT INTO `snakr_citylog` VALUES (264644893874197263,'ashburn'),(783498100259404515,'birmingham'),(1456401189262367458,'unknown'),(1592458084700052860,'washington'),(1651370235452053778,'?'),(1758163804100635462,'atlanta'),(1760059080499149476,'san francisco'),(2204009259228876401,'boardman'),(2869671789863365759,'san jose'),(3996774802115322208,'new york');
/*!40000 ALTER TABLE `snakr_citylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `snakr_countrylog`
--

DROP TABLE IF EXISTS `snakr_countrylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snakr_countrylog` (
  `id` bigint(20) NOT NULL,
  `country` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `snakr_countrylog`
--
-- ORDER BY:  `id`

LOCK TABLES `snakr_countrylog` WRITE;
/*!40000 ALTER TABLE `snakr_countrylog` DISABLE KEYS */;
INSERT INTO `snakr_countrylog` VALUES (3888491834616974882,'zz'),(3930169824901412938,'us');
/*!40000 ALTER TABLE `snakr_countrylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `snakr_eventlog`
--

DROP TABLE IF EXISTS `snakr_eventlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snakr_eventlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `logged_on` datetime(6) NOT NULL,
  `event_type` varchar(1) NOT NULL,
  `http_status_code` int(11) NOT NULL,
  `message` varchar(8192) NOT NULL,
  `longurl_id` bigint(20) NOT NULL,
  `shorturl_id` bigint(20) NOT NULL,
  `ip_id` bigint(20) NOT NULL,
  `lat` decimal(10,8) NOT NULL,
  `lng` decimal(11,8) NOT NULL,
  `city_id` bigint(20) NOT NULL,
  `country_id` bigint(20) NOT NULL,
  `host_id` bigint(20) NOT NULL,
  `useragent_id` bigint(20) NOT NULL,
  `referer` varchar(2083) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snakr_hostlog`
--

DROP TABLE IF EXISTS `snakr_hostlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snakr_hostlog` (
  `id` bigint(20) NOT NULL,
  `host` varchar(253) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `snakr_iplog`
--

DROP TABLE IF EXISTS `snakr_iplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snakr_iplog` (
  `id` bigint(20) NOT NULL,
  `ip` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `snakr_log`
--

DROP TABLE IF EXISTS `snakr_log`;
/*!50001 DROP VIEW IF EXISTS `snakr_log`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `snakr_log` AS SELECT 
 1 AS `eventlog_id`,
 1 AS `logged_on`,
 1 AS `event_type`,
 1 AS `http_status_code`,
 1 AS `longurl`,
 1 AS `longurl_created_on`,
 1 AS `shorturl`,
 1 AS `shorturl_created_on`,
 1 AS `is_active`,
 1 AS `compression_ratio`,
 1 AS `ip`,
 1 AS `city`,
 1 AS `country`,
 1 AS `host`,
 1 AS `useragent`,
 1 AS `message`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `snakr_longurls`
--

DROP TABLE IF EXISTS `snakr_longurls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snakr_longurls` (
  `id` bigint(20) NOT NULL,
  `longurl` varchar(4096) NOT NULL,
  `created_on` datetime NOT NULL,
  `originally_encoded` char(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snakr_shorturls`
--

DROP TABLE IF EXISTS `snakr_shorturls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snakr_useragentlog`
--

DROP TABLE IF EXISTS `snakr_useragentlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snakr_useragentlog` (
  `id` bigint(20) NOT NULL,
  `useragent` varchar(8192) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


ALTER TABLE `snakr_citylog`
ADD COLUMN `is_blacklisted` CHAR(1) NULL DEFAULT 'N';

ALTER TABLE `snakr_countrylog`
ADD COLUMN `is_blacklisted` CHAR(1) NULL DEFAULT 'N';

ALTER TABLE `snakr_hostlog`
ADD COLUMN `is_blacklisted` CHAR(1) NULL DEFAULT 'N';

ALTER TABLE `snakr_iplog`
ADD COLUMN `is_blacklisted` CHAR(1) NULL DEFAULT 'N';

ALTER TABLE `snakr_useragentlog`
ADD COLUMN `is_blacklisted` CHAR(1) NULL DEFAULT 'N';

--
-- Final view structure for view `snakr_log`
--

/*!50001 DROP VIEW IF EXISTS `snakr_log`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`snakrdbo`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `snakr_log` AS select `el`.`id` AS `eventlog_id`,`el`.`logged_on` AS `logged_on`,`el`.`event_type` AS `event_type`,`el`.`http_status_code` AS `http_status_code`,`lng`.`longurl` AS `longurl`,`lng`.`created_on` AS `longurl_created_on`,`sho`.`shorturl` AS `shorturl`,`sho`.`created_on` AS `shorturl_created_on`,`sho`.`is_active` AS `is_active`,`sho`.`compression_ratio` AS `compression_ratio`,`il`.`ip` AS `ip`,`cl`.`city` AS `city`,`kl`.`country` AS `country`,`hl`.`host` AS `host`,`uap`.`useragent` AS `useragent`,`el`.`message` AS `message` from (((((((`snakr_eventlog` `el` left join `snakr_longurls` `lng` on((`lng`.`id` = `el`.`longurl_id`))) left join `snakr_shorturls` `sho` on((`sho`.`id` = `el`.`shorturl_id`))) left join `snakr_iplog` `il` on((`il`.`id` = `el`.`ip_id`))) left join `snakr_citylog` `cl` on((`cl`.`id` = `el`.`city_id`))) left join `snakr_countrylog` `kl` on((`kl`.`id` = `el`.`country_id`))) left join `snakr_hostlog` `hl` on((`hl`.`id` = `el`.`host_id`))) left join `snakr_useragentlog` `uap` on((`uap`.`id` = `el`.`useragent_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-13 11:37:29
