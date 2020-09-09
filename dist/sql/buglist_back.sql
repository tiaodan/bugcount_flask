/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50621
Source Host           : localhost:3306
Source Database       : bugcount

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2020-06-01 21:43:56
*/

SET FOREIGN_KEY_CHECKS=0;

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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of buglist
-- ----------------------------
INSERT INTO `buglist` VALUES ('7', '2020-01-16', '1808', 'icss', 'icss_disp_20200114', 'bug71', '1', '2', '1', '1', '2020-01-10', 'icss_disp_20200114', '因为', '/home/bug_count/7.png', '/home/bug_count/7.png', '刘明乾', '备注', '2020-01-16', '7', '第一次备注', '2020-01-16', '7', '第二次备注', '2020-01-16', '7', '第三次备注');
INSERT INTO `buglist` VALUES ('8', '2020-01-17', '1808', 'icss', 'icss_disp_20200115', 'bug8', '1', '2', '1', '4', '2020-01-10', 'icss_disp_20200115', '因为', '/home/bug_count/8.png', '/home/bug_count/8.png', '李东东', '备注', '2020-01-17', '8', '第一次备注', '2020-01-17', '8', '第二次备注', '2020-01-17', '8', '第三次备注');
INSERT INTO `buglist` VALUES ('9', '2020-01-18', '1808', 'icss', 'icss_disp_20200116', 'bug9', '2', '2', '1', '2', '2020-01-10', 'icss_disp_20200116', '因为', '/home/bug_count/9.png', '/home/bug_count/9.png', '李东东', '备注', '2020-01-18', '9', '第一次备注', '2020-01-18', '9', '第二次备注', '2020-01-18', '9', '第三次备注');
INSERT INTO `buglist` VALUES ('10', '2020-01-19', '1808', 'icss', 'icss_disp_20200117', 'bug10', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200117', '因为', '/home/bug_count/10.png', '/home/bug_count/10.png', '李东东', '备注', '2020-01-19', '10', '第一次备注', '2020-01-19', '10', '第二次备注', '2020-01-19', '10', '第三次备注');
INSERT INTO `buglist` VALUES ('11', '2020-01-20', '1808', 'icss', 'icss_disp_20200118', 'bug11', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200118', '因为', '/home/bug_count/11.png', '/home/bug_count/11.png', '李东东', '备注', '2020-01-20', '11', '第一次备注', '2020-01-20', '11', '第二次备注', '2020-01-20', '11', '第三次备注');
INSERT INTO `buglist` VALUES ('12', '2020-01-21', '1808', 'icss', 'icss_disp_20200119', 'bug12', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200119', '因为', '/home/bug_count/12.png', '/home/bug_count/12.png', '李东东', '备注', '2020-01-21', '12', '第一次备注', '2020-01-21', '12', '第二次备注', '2020-01-21', '12', '第三次备注');
INSERT INTO `buglist` VALUES ('13', '2020-01-22', '1808', 'icss', 'icss_disp_20200120', 'bug13', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200120', '因为', '/home/bug_count/13.png', '/home/bug_count/13.png', '李东东', '备注', '2020-01-22', '13', '第一次备注', '2020-01-22', '13', '第二次备注', '2020-01-22', '13', '第三次备注');
INSERT INTO `buglist` VALUES ('14', '2020-01-23', '1808', 'icss', 'icss_disp_20200121', 'bug14', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200121', '因为', '/home/bug_count/14.png', '/home/bug_count/14.png', '韩扩华', '备注', '2020-01-23', '14', '第一次备注', '2020-01-23', '14', '第二次备注', '2020-01-23', '14', '第三次备注');
INSERT INTO `buglist` VALUES ('15', '2020-01-24', '1808', 'icss', 'icss_disp_20200122', 'bug15', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200108', '因为', '/home/bug_count/1.png', '/home/bug_count/1.png', '李东东', '备注', '2020-01-10', '1', '第一次备注', '2020-01-10', '1', '第二次备注', '2020-01-10', '1', '第三次备注');
INSERT INTO `buglist` VALUES ('16', '2020-01-10', '1808', 'icss', 'icss_disp_20200108', 'bug1', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200108', '因为', '/home/bug_count/1.png', '/home/bug_count/1.png', '李东东', '备注', '2020-01-10', '1', '第一次备注', '2020-01-10', '1', '第二次备注', '2020-01-10', '1', '第三次备注');
INSERT INTO `buglist` VALUES ('17', '2020-01-11', '1809', 'icss', 'icss_disp_20200109', 'bug2', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200109', '因为', '/home/bug_count/2.png', '/home/bug_count/2.png', '张三', '备注', '2020-01-11', '2', '第一次备注', '2020-01-11', '2', '第二次备注', '2020-01-11', '2', '第三次备注');
INSERT INTO `buglist` VALUES ('18', '2020-01-12', '1810', 'icss', 'icss_disp_20200110', 'bug3', '2', '2', '1', '4', '2020-01-10', 'icss_disp_20200110', '因为', '/home/bug_count/3.png', '/home/bug_count/3.png', '李东东', '备注', '2020-01-12', '3', '第一次备注', '2020-01-12', '3', '第二次备注', '2020-01-12', '3', '第三次备注');
INSERT INTO `buglist` VALUES ('19', '2020-01-13', '1811', 'icss', 'icss_disp_20200111', 'bug4', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200111', '因为', '/home/bug_count/4.png', '/home/bug_count/4.png', '李东东', '备注', '2020-01-13', '4', '第一次备注', '2020-01-13', '4', '第二次备注', '2020-01-13', '4', '第三次备注');
INSERT INTO `buglist` VALUES ('20', '2020-01-14', '1812', 'icss', 'icss_disp_20200112', 'bug5', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200112', '因为', '/home/bug_count/5.png', '/home/bug_count/5.png', '李东东', '备注', '2020-01-14', '5', '第一次备注', '2020-01-14', '5', '第二次备注', '2020-01-14', '5', '第三次备注');
INSERT INTO `buglist` VALUES ('21', '2020-01-15', '1813', 'icss', 'icss_disp_20200113', 'bug6', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200113', '因为', '/home/bug_count/6.png', '/home/bug_count/6.png', '李东东', '备注', '2020-01-15', '6', '第一次备注', '2020-01-15', '6', '第二次备注', '2020-01-15', '6', '第三次备注');
INSERT INTO `buglist` VALUES ('22', '2020-01-16', '1814', 'icss', 'icss_disp_20200114', 'bug7', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200114', '因为', '/home/bug_count/7.png', '/home/bug_count/7.png', '李东东', '备注', '2020-01-16', '7', '第一次备注', '2020-01-16', '7', '第二次备注', '2020-01-16', '7', '第三次备注');
INSERT INTO `buglist` VALUES ('23', '2020-01-17', '1815', 'icss', 'icss_disp_20200115', 'bug8', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200115', '因为', '/home/bug_count/8.png', '/home/bug_count/8.png', '李东东', '备注', '2020-01-17', '8', '第一次备注', '2020-01-17', '8', '第二次备注', '2020-01-17', '8', '第三次备注');
INSERT INTO `buglist` VALUES ('24', '2020-01-18', '1816', 'icss', 'icss_disp_20200116', 'bug9', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200116', '因为', '/home/bug_count/9.png', '/home/bug_count/9.png', '赵豪豪', '备注', '2020-01-18', '9', '第一次备注', '2020-01-18', '9', '第二次备注', '2020-01-18', '9', '第三次备注');
INSERT INTO `buglist` VALUES ('25', '2020-01-19', '1817', 'icss', 'icss_disp_20200117', 'bug10', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200117', '因为', '/home/bug_count/10.png', '/home/bug_count/10.png', '李东东', '备注', '2020-01-19', '10', '第一次备注', '2020-01-19', '10', '第二次备注', '2020-01-19', '10', '第三次备注');
INSERT INTO `buglist` VALUES ('26', '2020-01-20', '1818', 'icss', 'icss_disp_20200118', 'bug11', '3', '2', '1', '1', '2020-01-10', 'icss_disp_20200118', '因为', '/home/bug_count/11.png', '/home/bug_count/11.png', '韩扩华', '备注', '2020-01-20', '11', '第一次备注', '2020-01-20', '11', '第二次备注', '2020-01-20', '11', '第三次备注');
INSERT INTO `buglist` VALUES ('27', '2020-01-21', '1819', 'icss', 'icss_disp_20200119', 'bug12', '2', '2', '1', '1', '2020-01-10', 'icss_disp_20200119', '因为', '/home/bug_count/12.png', '/home/bug_count/12.png', '韩扩华', '备注', '2020-01-21', '12', '第一次备注', '2020-01-21', '12', '第二次备注', '2020-01-21', '12', '第三次备注');
INSERT INTO `buglist` VALUES ('28', '2020-01-22', '1820', 'icss', 'icss_disp_20200120', 'bug13', '2', '2', '1', '3', '2020-01-10', 'icss_disp_20200120', '因为', '/home/bug_count/13.png', '/home/bug_count/13.png', '韩扩华', '备注', '2020-01-22', '13', '第一次备注', '2020-01-22', '13', '第二次备注', '2020-01-22', '13', '第三次备注');
INSERT INTO `buglist` VALUES ('29', '2020-01-23', '1821', 'icss', 'icss_disp_20200121', 'bug14', '3', '2', '1', '3', '2020-01-10', 'icss_disp_20200121', '因为', '/home/bug_count/14.png', '/home/bug_count/14.png', '李东东', '备注', '2020-01-23', '14', '第一次备注', '2020-01-23', '14', '第二次备注', '2020-01-23', '14', '第三次备注');
INSERT INTO `buglist` VALUES ('30', '2020-01-24', '1822', 'icss', 'icss_disp_20200122', 'bug15', '3', '2', '1', '2', '2020-01-10', 'icss_disp_20200108', '因为', '/home/bug_count/1.png', '/home/bug_count/1.png', '李东东', '备注', '2020-01-10', '1', '第一次备注', '2020-01-10', '1', '第二次备注', '2020-01-10', '1', '第三次备注');
INSERT INTO `buglist` VALUES ('31', '2020-01-01', '1808', '1111', '1111', '1', '1', '1', '1', '1', '2020-01-01', '1', '1', '1', '1', '2', '1', '2020-01-01', '1', '', '2020-01-01', null, '', '2020-01-01', null, '');
