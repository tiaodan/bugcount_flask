/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : hahahh

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2020-09-24 11:40:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `announcement`
-- ----------------------------
DROP TABLE IF EXISTS `announcement`;
CREATE TABLE `announcement` (
  `announcementid` int(10) NOT NULL AUTO_INCREMENT,
  `announcement` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`announcementid`),
  KEY `announcementid` (`announcementid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of announcement
-- ----------------------------
INSERT INTO `announcement` VALUES ('1', '公告内容1：2020-09-10 恭喜项目1圆满完成，大家放假一天');
INSERT INTO `announcement` VALUES ('2', '公告内容2222');
INSERT INTO `announcement` VALUES ('3', '公告内容33333');
