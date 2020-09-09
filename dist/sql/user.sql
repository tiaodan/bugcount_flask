/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.156
Source Server Version : 50173
Source Host           : 192.168.1.156:3306
Source Database       : myomc

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2020-07-15 16:45:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'nouser', 'a249681c33f044bc05b93c7ed4f4c482');
INSERT INTO `user` VALUES ('9', 'admin', '5f4dcc3b5aa765d61d8327deb882cf99');
INSERT INTO `user` VALUES ('8', 'user', '5f4dcc3b5aa765d61d8327deb882cf99');
