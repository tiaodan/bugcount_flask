/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.156
Source Server Version : 50173
Source Host           : 192.168.1.156:3306
Source Database       : myomc

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2020-07-15 16:46:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `role`
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('7', 'admin', 'admin');
INSERT INTO `role` VALUES ('6', 'user', 'user');
