/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : hahahh

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2020-09-24 11:39:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
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

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('71', 'admin1', 'd31e0583cf78a28a4a6e7692e2f4a588', '221', '34234@123.com', '2', null, '12313', '1');
INSERT INTO `user` VALUES ('72', 'admin2', '885ee4b6ee92fc9aba945f2641fa3eca', 'admin23666', 'admin2@sunksisen.com', '2', '2020-01-02', 'nosession', '1');
INSERT INTO `user` VALUES ('73', 'admin3', '32cacb2f994f6b42183a1300d9a3e8d6', 'admin3', 'admin3@123.com', '2', '2020-01-03', 'no', '1');
INSERT INTO `user` VALUES ('74', 'admin4', 'fc1ebc848e31e0a68e868432225e3c82', 'admin4', 'admin4@123.com', '2', null, '', '1');
INSERT INTO `user` VALUES ('75', 'admin5', '26a91342190d515231d7238b0c5438e1', 'admin5', 'admin5@123.com', '2', '2020-01-05', '', '1');
INSERT INTO `user` VALUES ('76', 'test11', 'f696282aa4cd4f614aa995190cf442fe', 'test11', 'test11@123.com', '2', '2020-05-30', 'ss', '2');
INSERT INTO `user` VALUES ('78', 'test55', '7e39cfce74d155294619613f42484f18', null, null, null, null, null, '1');
INSERT INTO `user` VALUES ('79', 'test66', '3f1bc06510a4e5ac9bd49f64d247354c', 'test66', 'test66@123.com', '2', null, '', '2');
INSERT INTO `user` VALUES ('80', 'test77', 'd40b31764c7f77dad3fa57e01d2c19fd', '', 'test77@123.com', '2', null, '', '2');
INSERT INTO `user` VALUES ('81', '11111111', 'bbb8aae57c104cda40c93843ad5e6db8', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('82', 'test88', '841f54c24fd24fb27f45377b2e941070', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('84', 'admin11', 'e020590f0e18cd6053d7ae0e0a507609', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('85', 'admin12', '1844156d4166d94387f1a4ad031ca5fa', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('86', 'admin13', '588e57b852a16b297af73ae818065474', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('89', 'admin9', 'eed57216df3731106517ccaf5da2122d', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('90', 'test12', '60474c9c10d7142b7508ce7a50acf414', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('91', 'adminm', 'c8d32c2a41fc240a82ea6e2d1566e8ef', null, null, null, null, null, '2');
INSERT INTO `user` VALUES ('92', 'liutan', 'f09d477dee23537565a95bd84b2a9e51', null, null, null, null, null, '2');
