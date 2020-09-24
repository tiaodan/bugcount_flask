/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.7.17-log : Database - bugcount
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `announcement` */

DROP TABLE IF EXISTS `announcement`;

CREATE TABLE `announcement` (
  `announcementid` int(10) NOT NULL AUTO_INCREMENT,
  `announcement` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`announcementid`),
  KEY `announcementid` (`announcementid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Table structure for table `backup_record` */

DROP TABLE IF EXISTS `backup_record`;

CREATE TABLE `backup_record` (
  `backup_id` int(11) NOT NULL AUTO_INCREMENT,
  `backup_path` varchar(1024) DEFAULT NULL,
  `backup_user` varchar(64) DEFAULT NULL,
  `backup_date` date DEFAULT NULL,
  PRIMARY KEY (`backup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `bugimg` */

DROP TABLE IF EXISTS `bugimg`;

CREATE TABLE `bugimg` (
  `imgid` int(11) NOT NULL AUTO_INCREMENT,
  `img_path` varchar(1024) DEFAULT NULL,
  `img_remrk` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`imgid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `buglist` */

DROP TABLE IF EXISTS `buglist`;

CREATE TABLE `buglist` (
  `bugid` int(11) NOT NULL AUTO_INCREMENT,
  `bug_submit_date` date DEFAULT NULL,
  `project` varchar(64) DEFAULT NULL,
  `software` varchar(64) DEFAULT NULL,
  `test_version` varchar(128) DEFAULT NULL,
  `bug_description` varchar(3072) NOT NULL,
  `severity_level` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `bug_difficulty` int(11) DEFAULT NULL,
  `bug_status` int(11) DEFAULT NULL,
  `bug_close_date` date DEFAULT NULL,
  `close_version` varchar(128) DEFAULT NULL,
  `cause_analysis` varchar(1024) DEFAULT NULL,
  `bug_img` varchar(256) DEFAULT NULL,
  `intermediate_situation` varchar(1024) DEFAULT NULL,
  `developer` varchar(64) DEFAULT NULL,
  `remark` varchar(1024) DEFAULT NULL,
  `regression_times` int(11) DEFAULT NULL,
  `reopen_times` int(11) DEFAULT NULL,
  `submitterindex` varchar(1024) NOT NULL,
  PRIMARY KEY (`bugid`),
  UNIQUE KEY `submitterindex` (`submitterindex`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=32410 DEFAULT CHARSET=utf8;

/*Table structure for table `edit_record` */

DROP TABLE IF EXISTS `edit_record`;

CREATE TABLE `edit_record` (
  `edit_record_id` int(11) NOT NULL AUTO_INCREMENT,
  `edit_bug_id` int(11) DEFAULT NULL,
  `edit_user` varchar(64) DEFAULT NULL,
  `edit_time` date DEFAULT NULL,
  PRIMARY KEY (`edit_record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `privilege` */

DROP TABLE IF EXISTS `privilege`;

CREATE TABLE `privilege` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `leaf` tinyint(4) DEFAULT NULL,
  `parentId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `parentId` (`parentId`)
) ENGINE=MyISAM AUTO_INCREMENT=195 DEFAULT CHARSET=utf8;

/*Table structure for table `role` */

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Table structure for table `role_privilege` */

DROP TABLE IF EXISTS `role_privilege`;

CREATE TABLE `role_privilege` (
  `roleId` int(11) NOT NULL,
  `privilegeId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`privilegeId`),
  UNIQUE KEY `privilegeId` (`roleId`,`privilegeId`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `user_remark` varchar(64) DEFAULT NULL,
  `user_email` varchar(64) DEFAULT NULL,
  `user_level` int(11) DEFAULT NULL,
  `create_time` date DEFAULT NULL,
  `session` varchar(1024) DEFAULT NULL,
  `roleId` varchar(11) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
