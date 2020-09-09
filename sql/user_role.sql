/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.156
Source Server Version : 50173
Source Host           : 192.168.1.156:3306
Source Database       : myomc

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2020-07-15 16:45:46
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `user_role`
-- ----------------------------
DROP TABLE IF EXISTS `user_role`;
CREATE TABLE `user_role` (
  `userId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  PRIMARY KEY (`userId`,`roleId`),
  KEY `roleId` (`roleId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_role
-- ----------------------------
INSERT INTO `user_role` VALUES ('8', '6');
INSERT INTO `user_role` VALUES ('9', '7');
