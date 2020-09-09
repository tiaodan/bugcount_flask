/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50727
Source Host           : localhost:3306
Source Database       : bugcount

Target Server Type    : MYSQL
Target Server Version : 50727
File Encoding         : 65001

Date: 2020-07-16 11:27:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `role_privilege`
-- ----------------------------
DROP TABLE IF EXISTS `role_privilege`;
CREATE TABLE `role_privilege` (
  `roleId` int(11) NOT NULL,
  `privilegeId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`privilegeId`),
  KEY `privilegeId` (`privilegeId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role_privilege
-- ----------------------------
INSERT INTO `role_privilege` VALUES ('1', '1');
INSERT INTO `role_privilege` VALUES ('1', '2');
INSERT INTO `role_privilege` VALUES ('1', '3');
INSERT INTO `role_privilege` VALUES ('1', '4');
INSERT INTO `role_privilege` VALUES ('1', '5');
INSERT INTO `role_privilege` VALUES ('1', '6');
INSERT INTO `role_privilege` VALUES ('1', '7');
INSERT INTO `role_privilege` VALUES ('1', '8');
INSERT INTO `role_privilege` VALUES ('1', '9');
INSERT INTO `role_privilege` VALUES ('1', '10');
INSERT INTO `role_privilege` VALUES ('1', '11');
INSERT INTO `role_privilege` VALUES ('1', '21');
INSERT INTO `role_privilege` VALUES ('1', '31');
INSERT INTO `role_privilege` VALUES ('1', '32');
INSERT INTO `role_privilege` VALUES ('1', '33');
INSERT INTO `role_privilege` VALUES ('1', '34');
INSERT INTO `role_privilege` VALUES ('1', '35');
INSERT INTO `role_privilege` VALUES ('1', '36');
INSERT INTO `role_privilege` VALUES ('1', '37');
INSERT INTO `role_privilege` VALUES ('1', '38');
INSERT INTO `role_privilege` VALUES ('1', '39');
INSERT INTO `role_privilege` VALUES ('1', '51');

INSERT INTO `role_privilege` VALUES ('2', '1');
INSERT INTO `role_privilege` VALUES ('2', '2');
INSERT INTO `role_privilege` VALUES ('2', '3');
INSERT INTO `role_privilege` VALUES ('2', '4');
INSERT INTO `role_privilege` VALUES ('2', '5');
INSERT INTO `role_privilege` VALUES ('2', '6');
INSERT INTO `role_privilege` VALUES ('2', '7');
INSERT INTO `role_privilege` VALUES ('2', '8');
INSERT INTO `role_privilege` VALUES ('2', '9');
INSERT INTO `role_privilege` VALUES ('2', '10');
INSERT INTO `role_privilege` VALUES ('2', '11');
INSERT INTO `role_privilege` VALUES ('2', '21');
INSERT INTO `role_privilege` VALUES ('2', '31');
INSERT INTO `role_privilege` VALUES ('2', '32');
INSERT INTO `role_privilege` VALUES ('2', '33');
INSERT INTO `role_privilege` VALUES ('2', '34');
INSERT INTO `role_privilege` VALUES ('2', '35');
INSERT INTO `role_privilege` VALUES ('2', '36');
INSERT INTO `role_privilege` VALUES ('2', '37');
INSERT INTO `role_privilege` VALUES ('2', '38');
INSERT INTO `role_privilege` VALUES ('2', '39');
INSERT INTO `role_privilege` VALUES ('2', '51');
