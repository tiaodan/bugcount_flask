/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50621
Source Host           : localhost:3306
Source Database       : bugcount

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2020-05-23 07:51:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `backup_record`
-- ----------------------------
DROP TABLE IF EXISTS `backup_record`;
CREATE TABLE `backup_record` (
  `backup_id` int(11) NOT NULL AUTO_INCREMENT,
  `backup_path` varchar(1024) DEFAULT NULL,
  `backup_user` varchar(64) DEFAULT NULL,
  `backup_date` date DEFAULT NULL,
  PRIMARY KEY (`backup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of backup_record
-- ----------------------------

-- ----------------------------
-- Table structure for `bugimg`
-- ----------------------------
DROP TABLE IF EXISTS `bugimg`;
CREATE TABLE `bugimg` (
  `imgid` int(11) NOT NULL AUTO_INCREMENT,
  `img_path` varchar(1024) DEFAULT NULL,
  `img_remrk` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`imgid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of bugimg
-- ----------------------------

-- ----------------------------
-- Table structure for `buglist`
-- ----------------------------
DROP TABLE IF EXISTS `buglist`;
CREATE TABLE `buglist` (
  `bugid` int(11) NOT NULL AUTO_INCREMENT,
  `bug_submit_date` date DEFAULT NULL,
  `project` varchar(64) DEFAULT NULL,
  `software` varchar(64) DEFAULT NULL,
  `test_version` varchar(128) DEFAULT NULL,
  `bug_description` varchar(1024) DEFAULT NULL,
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
  `first_bug_regression_date` date DEFAULT NULL,
  `first_bug_regression_status` int(11) DEFAULT NULL,
  `first_bug_regression_remark` varchar(1024) DEFAULT NULL,
  `second_bug_regression_date` date DEFAULT NULL,
  `second_bug_regression_status` int(11) DEFAULT NULL,
  `second_bug_regression_remark` varchar(1024) DEFAULT NULL,
  `third_bug_regression_date` date DEFAULT NULL,
  `third_bug_regression_status` int(11) DEFAULT NULL,
  `third_bug_regression_remark` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`bugid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of buglist
-- ----------------------------
INSERT INTO `buglist` VALUES ('1', '2020-01-10', '1808', 'icss', 'icss_disp_20200108', 'bug1', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200108', '因为', '/home/bug_count/1.png', '/home/bug_count/1.png', '李东东', '备注', '2020-01-10', '1', '第一次备注', '2020-01-10', '1', '第二次备注', '2020-01-10', '1', '第三次备注');
INSERT INTO `buglist` VALUES ('2', '2020-01-11', '1808', 'icss', 'icss_disp_20200109', 'bug2', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200109', '因为', '/home/bug_count/2.png', '/home/bug_count/2.png', '李东东', '备注', '2020-01-11', '2', '第一次备注', '2020-01-11', '2', '第二次备注', '2020-01-11', '2', '第三次备注');
INSERT INTO `buglist` VALUES ('3', '2020-01-12', '1808', 'icss', 'icss_disp_20200110', 'bug3', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200110', '因为', '/home/bug_count/3.png', '/home/bug_count/3.png', '李东东', '备注', '2020-01-12', '3', '第一次备注', '2020-01-12', '3', '第二次备注', '2020-01-12', '3', '第三次备注');
INSERT INTO `buglist` VALUES ('4', '2020-01-13', '1808', 'icss', 'icss_disp_20200111', 'bug4', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200111', '因为', '/home/bug_count/4.png', '/home/bug_count/4.png', '李东东', '备注', '2020-01-13', '4', '第一次备注', '2020-01-13', '4', '第二次备注', '2020-01-13', '4', '第三次备注');
INSERT INTO `buglist` VALUES ('5', '2020-01-14', '1808', 'icss', 'icss_disp_20200112', 'bug5', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200112', '因为', '/home/bug_count/5.png', '/home/bug_count/5.png', '李东东', '备注', '2020-01-14', '5', '第一次备注', '2020-01-14', '5', '第二次备注', '2020-01-14', '5', '第三次备注');
INSERT INTO `buglist` VALUES ('6', '2020-01-15', '1808', 'icss', 'icss_disp_20200113', 'bug6', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200113', '因为', '/home/bug_count/6.png', '/home/bug_count/6.png', '李东东', '备注', '2020-01-15', '6', '第一次备注', '2020-01-15', '6', '第二次备注', '2020-01-15', '6', '第三次备注');
INSERT INTO `buglist` VALUES ('7', '2020-01-16', '1808', 'icss', 'icss_disp_20200114', 'bug7', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200114', '因为', '/home/bug_count/7.png', '/home/bug_count/7.png', '李东东', '备注', '2020-01-16', '7', '第一次备注', '2020-01-16', '7', '第二次备注', '2020-01-16', '7', '第三次备注');
INSERT INTO `buglist` VALUES ('8', '2020-01-17', '1808', 'icss', 'icss_disp_20200115', 'bug8', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200115', '因为', '/home/bug_count/8.png', '/home/bug_count/8.png', '李东东', '备注', '2020-01-17', '8', '第一次备注', '2020-01-17', '8', '第二次备注', '2020-01-17', '8', '第三次备注');
INSERT INTO `buglist` VALUES ('9', '2020-01-18', '1808', 'icss', 'icss_disp_20200116', 'bug9', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200116', '因为', '/home/bug_count/9.png', '/home/bug_count/9.png', '李东东', '备注', '2020-01-18', '9', '第一次备注', '2020-01-18', '9', '第二次备注', '2020-01-18', '9', '第三次备注');
INSERT INTO `buglist` VALUES ('10', '2020-01-19', '1808', 'icss', 'icss_disp_20200117', 'bug10', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200117', '因为', '/home/bug_count/10.png', '/home/bug_count/10.png', '李东东', '备注', '2020-01-19', '10', '第一次备注', '2020-01-19', '10', '第二次备注', '2020-01-19', '10', '第三次备注');
INSERT INTO `buglist` VALUES ('11', '2020-01-20', '1808', 'icss', 'icss_disp_20200118', 'bug11', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200118', '因为', '/home/bug_count/11.png', '/home/bug_count/11.png', '李东东', '备注', '2020-01-20', '11', '第一次备注', '2020-01-20', '11', '第二次备注', '2020-01-20', '11', '第三次备注');
INSERT INTO `buglist` VALUES ('12', '2020-01-21', '1808', 'icss', 'icss_disp_20200119', 'bug12', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200119', '因为', '/home/bug_count/12.png', '/home/bug_count/12.png', '李东东', '备注', '2020-01-21', '12', '第一次备注', '2020-01-21', '12', '第二次备注', '2020-01-21', '12', '第三次备注');
INSERT INTO `buglist` VALUES ('13', '2020-01-22', '1808', 'icss', 'icss_disp_20200120', 'bug13', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200120', '因为', '/home/bug_count/13.png', '/home/bug_count/13.png', '李东东', '备注', '2020-01-22', '13', '第一次备注', '2020-01-22', '13', '第二次备注', '2020-01-22', '13', '第三次备注');
INSERT INTO `buglist` VALUES ('14', '2020-01-23', '1808', 'icss', 'icss_disp_20200121', 'bug14', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200121', '因为', '/home/bug_count/14.png', '/home/bug_count/14.png', '李东东', '备注', '2020-01-23', '14', '第一次备注', '2020-01-23', '14', '第二次备注', '2020-01-23', '14', '第三次备注');
INSERT INTO `buglist` VALUES ('15', '2020-01-24', '1808', 'icss', 'icss_disp_20200122', 'bug15', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200108', '因为', '/home/bug_count/1.png', '/home/bug_count/1.png', '李东东', '备注', '2020-01-10', '1', '第一次备注', '2020-01-10', '1', '第二次备注', '2020-01-10', '1', '第三次备注');
INSERT INTO `buglist` VALUES ('16', '2020-01-10', '1808', 'icss', 'icss_disp_20200108', 'bug1', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200108', '因为', '/home/bug_count/1.png', '/home/bug_count/1.png', '李东东', '备注', '2020-01-10', '1', '第一次备注', '2020-01-10', '1', '第二次备注', '2020-01-10', '1', '第三次备注');
INSERT INTO `buglist` VALUES ('17', '2020-01-11', '1809', 'icss', 'icss_disp_20200109', 'bug2', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200109', '因为', '/home/bug_count/2.png', '/home/bug_count/2.png', '张三', '备注', '2020-01-11', '2', '第一次备注', '2020-01-11', '2', '第二次备注', '2020-01-11', '2', '第三次备注');
INSERT INTO `buglist` VALUES ('18', '2020-01-12', '1810', 'icss', 'icss_disp_20200110', 'bug3', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200110', '因为', '/home/bug_count/3.png', '/home/bug_count/3.png', '李东东', '备注', '2020-01-12', '3', '第一次备注', '2020-01-12', '3', '第二次备注', '2020-01-12', '3', '第三次备注');
INSERT INTO `buglist` VALUES ('19', '2020-01-13', '1811', 'icss', 'icss_disp_20200111', 'bug4', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200111', '因为', '/home/bug_count/4.png', '/home/bug_count/4.png', '李东东', '备注', '2020-01-13', '4', '第一次备注', '2020-01-13', '4', '第二次备注', '2020-01-13', '4', '第三次备注');
INSERT INTO `buglist` VALUES ('20', '2020-01-14', '1812', 'icss', 'icss_disp_20200112', 'bug5', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200112', '因为', '/home/bug_count/5.png', '/home/bug_count/5.png', '李东东', '备注', '2020-01-14', '5', '第一次备注', '2020-01-14', '5', '第二次备注', '2020-01-14', '5', '第三次备注');
INSERT INTO `buglist` VALUES ('21', '2020-01-15', '1813', 'icss', 'icss_disp_20200113', 'bug6', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200113', '因为', '/home/bug_count/6.png', '/home/bug_count/6.png', '李东东', '备注', '2020-01-15', '6', '第一次备注', '2020-01-15', '6', '第二次备注', '2020-01-15', '6', '第三次备注');
INSERT INTO `buglist` VALUES ('22', '2020-01-16', '1814', 'icss', 'icss_disp_20200114', 'bug7', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200114', '因为', '/home/bug_count/7.png', '/home/bug_count/7.png', '李东东', '备注', '2020-01-16', '7', '第一次备注', '2020-01-16', '7', '第二次备注', '2020-01-16', '7', '第三次备注');
INSERT INTO `buglist` VALUES ('23', '2020-01-17', '1815', 'icss', 'icss_disp_20200115', 'bug8', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200115', '因为', '/home/bug_count/8.png', '/home/bug_count/8.png', '李东东', '备注', '2020-01-17', '8', '第一次备注', '2020-01-17', '8', '第二次备注', '2020-01-17', '8', '第三次备注');
INSERT INTO `buglist` VALUES ('24', '2020-01-18', '1816', 'icss', 'icss_disp_20200116', 'bug9', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200116', '因为', '/home/bug_count/9.png', '/home/bug_count/9.png', '李东东', '备注', '2020-01-18', '9', '第一次备注', '2020-01-18', '9', '第二次备注', '2020-01-18', '9', '第三次备注');
INSERT INTO `buglist` VALUES ('25', '2020-01-19', '1817', 'icss', 'icss_disp_20200117', 'bug10', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200117', '因为', '/home/bug_count/10.png', '/home/bug_count/10.png', '李东东', '备注', '2020-01-19', '10', '第一次备注', '2020-01-19', '10', '第二次备注', '2020-01-19', '10', '第三次备注');
INSERT INTO `buglist` VALUES ('26', '2020-01-20', '1818', 'icss', 'icss_disp_20200118', 'bug11', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200118', '因为', '/home/bug_count/11.png', '/home/bug_count/11.png', '李东东', '备注', '2020-01-20', '11', '第一次备注', '2020-01-20', '11', '第二次备注', '2020-01-20', '11', '第三次备注');
INSERT INTO `buglist` VALUES ('27', '2020-01-21', '1819', 'icss', 'icss_disp_20200119', 'bug12', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200119', '因为', '/home/bug_count/12.png', '/home/bug_count/12.png', '李东东', '备注', '2020-01-21', '12', '第一次备注', '2020-01-21', '12', '第二次备注', '2020-01-21', '12', '第三次备注');
INSERT INTO `buglist` VALUES ('28', '2020-01-22', '1820', 'icss', 'icss_disp_20200120', 'bug13', '3', '2', '1', '3', '2020-01-10', 'icss_disp_20200120', '因为', '/home/bug_count/13.png', '/home/bug_count/13.png', '李东东', '备注', '2020-01-22', '13', '第一次备注', '2020-01-22', '13', '第二次备注', '2020-01-22', '13', '第三次备注');
INSERT INTO `buglist` VALUES ('29', '2020-01-23', '1821', 'icss', 'icss_disp_20200121', 'bug14', '3', '2', '1', '3', '2020-01-10', 'icss_disp_20200121', '因为', '/home/bug_count/14.png', '/home/bug_count/14.png', '李东东', '备注', '2020-01-23', '14', '第一次备注', '2020-01-23', '14', '第二次备注', '2020-01-23', '14', '第三次备注');
INSERT INTO `buglist` VALUES ('30', '2020-01-24', '1822', 'icss', 'icss_disp_20200122', 'bug15', '3', '2', '1', '2', '2020-01-10', 'icss_disp_20200108', '因为', '/home/bug_count/1.png', '/home/bug_count/1.png', '李东东', '备注', '2020-01-10', '1', '第一次备注', '2020-01-10', '1', '第二次备注', '2020-01-10', '1', '第三次备注');

-- ----------------------------
-- Table structure for `edit_record`
-- ----------------------------
DROP TABLE IF EXISTS `edit_record`;
CREATE TABLE `edit_record` (
  `edit_record_id` int(11) NOT NULL AUTO_INCREMENT,
  `edit_bug_id` int(11) DEFAULT NULL,
  `edit_user` varchar(64) DEFAULT NULL,
  `edit_time` date DEFAULT NULL,
  PRIMARY KEY (`edit_record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of edit_record
-- ----------------------------

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
  `user_level` varchar(64) DEFAULT NULL,
  `create_time` date DEFAULT NULL,
  `session` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('23', 'root', 'pass', '118@123.com', '118@123.com', null, null, null);
INSERT INTO `user` VALUES ('28', 'admin1', '1a1dc91c907325c69271ddf0c944bc72', null, null, null, null, null);
INSERT INTO `user` VALUES ('29', 'admin0', '62f04a011fbb80030bb0a13701c20b41', null, null, null, null, null);
