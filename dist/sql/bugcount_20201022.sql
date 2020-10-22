/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50621
Source Host           : localhost:3306
Source Database       : bugcount

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2020-10-22 15:59:18
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
INSERT INTO `announcement` VALUES ('1', '公告内容1：2020-09-10 恭喜项目1圆满完成，大家放假一天!');
INSERT INTO `announcement` VALUES ('2', '公告内容2222');
INSERT INTO `announcement` VALUES ('3', '公告内容33333');

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
  `project` varchar(256) DEFAULT NULL,
  `software` varchar(256) DEFAULT NULL,
  `test_version` varchar(256) DEFAULT NULL,
  `bug_description` varchar(6144) NOT NULL,
  `severity_level` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `bug_difficulty` int(11) DEFAULT NULL,
  `bug_status` int(11) DEFAULT NULL,
  `bug_close_date` date DEFAULT NULL,
  `close_version` varchar(256) DEFAULT NULL,
  `cause_analysis` varchar(3072) DEFAULT NULL,
  `bug_img` varchar(1024) DEFAULT NULL,
  `intermediate_situation` varchar(1024) DEFAULT NULL,
  `developer` varchar(256) DEFAULT NULL,
  `remark` varchar(1024) DEFAULT NULL,
  `regression_times` int(11) DEFAULT NULL,
  `reopen_times` int(11) DEFAULT NULL,
  `submitterindex` varchar(80) NOT NULL,
  PRIMARY KEY (`bugid`),
  UNIQUE KEY `submitterindex` (`submitterindex`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=89722 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of buglist
-- ----------------------------

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
-- Table structure for `privilege`
-- ----------------------------
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

-- ----------------------------
-- Records of privilege
-- ----------------------------
INSERT INTO `privilege` VALUES ('1', 'AddQuickLink', '添加网址', 'quicklink/add', null, '1', null);
INSERT INTO `privilege` VALUES ('2', 'DeleteQuickLink', '删除网址', 'quicklink/delete', null, '1', '1');
INSERT INTO `privilege` VALUES ('3', 'UpdateQuickLink', '修改网址', 'quicklink/update', null, '1', '2');
INSERT INTO `privilege` VALUES ('4', 'ViewAllQuickLink', '查询所有网址', 'quicklink/viewAll', null, '1', '2');
INSERT INTO `privilege` VALUES ('5', 'ViewUserManualQuickLink', '查询用户手册网址', 'quicklink/viewUserManual', null, '1', '2');
INSERT INTO `privilege` VALUES ('6', 'ViewBugDefineRuleQuickLink', '查看bug定义规则网址', 'quicklink/viewbugDefineRule', null, '1', '2');
INSERT INTO `privilege` VALUES ('7', 'ViewTestlinkQuickLink', '查看testlink网址', 'quicklink/viewTestlink', null, '1', '1');
INSERT INTO `privilege` VALUES ('8', 'ViewRedmineQuickLink', '查看redmine网址', 'quicklink/viewRedmine', null, '1', '2');
INSERT INTO `privilege` VALUES ('9', 'ViewOAQuickLink', '查看OA网址', 'quicklink/viewOA', null, '1', '2');
INSERT INTO `privilege` VALUES ('10', 'ViewCompanyEmailQuickLink', '查看公司邮箱网址', 'quicklink/viewCompanyEmail', null, '1', '2');
INSERT INTO `privilege` VALUES ('11', 'ViewCompanyOfficialWebsiteQuickLink', '查看公司官网', 'quicklink/viewCompanyOfficialWebsite', null, '1', '1');
INSERT INTO `privilege` VALUES ('12', 'AddIMSUser', '预留到20', 'ims/add', null, '1', '11');
INSERT INTO `privilege` VALUES ('13', 'DeleteIMSUser', '预留到20', 'ims/delete', null, '1', '11');
INSERT INTO `privilege` VALUES ('14', 'UpdateIMSUser', '预留到20', 'ims/update', null, '1', '11');
INSERT INTO `privilege` VALUES ('15', 'ViewIMSUser', '预留到20', 'ims/list', null, '1', '11');
INSERT INTO `privilege` VALUES ('16', 'GroupCallGroupManage', '预留到20', 'hssGroup/listUI', null, '1', '1');
INSERT INTO `privilege` VALUES ('17', 'AddGroupCallGroup', '预留到20', 'hssGroup/add', null, '1', '16');
INSERT INTO `privilege` VALUES ('18', 'DeleteGroupCallGroup', '预留到20', 'hssGroup/delete', null, '1', '16');
INSERT INTO `privilege` VALUES ('19', 'UpdateGroupCallGroup', '预留到20', 'hssGroup/update', null, '1', '16');
INSERT INTO `privilege` VALUES ('20', 'ViewGroupCallGroup', '预留到20', 'hssGroup/list', null, '1', '16');
INSERT INTO `privilege` VALUES ('21', 'AllUserManage', '用户(增删改查)', 'user/all', null, '1', '1');
INSERT INTO `privilege` VALUES ('22', 'AddUser', '添加用户', 'user/add', null, '1', '21');
INSERT INTO `privilege` VALUES ('23', 'DeleteUser', '删用用户', 'user/delete', null, '1', '21');
INSERT INTO `privilege` VALUES ('24', 'UpdateUser', '修改用户', 'user/update', null, '1', '21');
INSERT INTO `privilege` VALUES ('25', 'ViewUser', '查看用户', 'user/view', null, '1', '21');
INSERT INTO `privilege` VALUES ('26', 'priorityManage', '预留到30', 'hss/listMdnUI', null, '1', '1');
INSERT INTO `privilege` VALUES ('27', 'priorityModifity', '预留到30', 'hss/updatePriority', null, '1', '26');
INSERT INTO `privilege` VALUES ('28', 'HssItemConf', '预留到30', 'hssParam/listUI', null, '1', '1');
INSERT INTO `privilege` VALUES ('29', 'HssParamUpdate', '预留到30', 'hssParam/update', null, '1', '28');
INSERT INTO `privilege` VALUES ('30', 'userGroupPriority1', '预留到30', 'hss/userGroupListUI', null, '1', '1');
INSERT INTO `privilege` VALUES ('31', 'AllBugManage', 'bug管理所有权限', null, null, '1', null);
INSERT INTO `privilege` VALUES ('32', 'AddBug', '新增bug', 'eth/listUI', null, '1', '31');
INSERT INTO `privilege` VALUES ('33', 'DeleteBug', '删除bug', 'omc/viewableDns', null, '1', '32');
INSERT INTO `privilege` VALUES ('34', 'UpdateBug', '修改bug', 'eth/activateUpdate', null, '1', '32');
INSERT INTO `privilege` VALUES ('35', 'BatchAddBug', '批量新增bug', 'batch/staticAdd', null, '1', '32');
INSERT INTO `privilege` VALUES ('36', 'BatchDeleteBug', '批量删除bug', 'eth/staticUpdate', null, '1', '32');
INSERT INTO `privilege` VALUES ('37', 'UploadBug', 'bug上传', 'eth/delete', null, '1', '32');
INSERT INTO `privilege` VALUES ('38', 'TruncateBuglist', 'bug清空', 'eth/active', null, '1', '32');
INSERT INTO `privilege` VALUES ('39', 'BugTemplateDownload', '批bug模板下载', 'eth/viewData', null, '1', '32');
INSERT INTO `privilege` VALUES ('40', 'YuLiu40', '预留到50', 'route/listUI40', null, '0', '31');
INSERT INTO `privilege` VALUES ('41', 'YuLiu41', '预留到50', 'route/listUI', null, '0', '31');
INSERT INTO `privilege` VALUES ('42', 'YuLiu42', '预留到50', 'route/defaultRoute', null, '1', '41');
INSERT INTO `privilege` VALUES ('43', 'YuLiu43', '预留到50', 'route/addRoute', null, '1', '41');
INSERT INTO `privilege` VALUES ('44', 'YuLiu44', '预留到50', 'route/viewData', null, '1', '41');
INSERT INTO `privilege` VALUES ('45', 'YuLiu45', '预留到50', 'route/deleteRoute', null, '1', '41');
INSERT INTO `privilege` VALUES ('46', 'YuLiu46', '预留到50', 'route/ospf', null, '1', '41');
INSERT INTO `privilege` VALUES ('47', 'YuLiu47', '预留到50', 'hostaddr/listUI', null, '0', '31');
INSERT INTO `privilege` VALUES ('48', 'YuLiu48', '预留到50', 'hostaddr/add', null, '1', '47');
INSERT INTO `privilege` VALUES ('49', 'YuLiu49', '预留到50', 'hostaddr/delete', null, '1', '47');
INSERT INTO `privilege` VALUES ('50', 'YuLiu50', '预留到50', 'hostaddr/view', null, '1', '47');
INSERT INTO `privilege` VALUES ('51', 'ViewBugMap', '统计图查询', 'dns/listUI', null, '1', '31');
INSERT INTO `privilege` VALUES ('52', 'YuLiu52', '预留到60', 'card/listUI', null, '0', '31');
INSERT INTO `privilege` VALUES ('53', 'YuLiu53', '预留到60', 'card/list', null, '1', '52');
INSERT INTO `privilege` VALUES ('54', 'YuLiu54', '预留到60', 'card/add', null, '1', '52');
INSERT INTO `privilege` VALUES ('55', 'YuLiu55', '预留到60', 'card/delete', null, '1', '52');
INSERT INTO `privilege` VALUES ('56', 'YuLiu56', '预留到60', 'dnsServer/listUI', null, '1', '31');
INSERT INTO `privilege` VALUES ('57', 'YuLiu57', '预留到60', 'license/listUI', null, '1', '31');
INSERT INTO `privilege` VALUES ('58', 'YuLiu58', '预留到60', 'card/sysListUI1', null, '1', '31');
INSERT INTO `privilege` VALUES ('59', 'YuLiu59', '预留到60', null, null, '0', null);
INSERT INTO `privilege` VALUES ('60', 'YuLiu60', '预留到60', 'module/listUI', null, '0', '59');

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
INSERT INTO `role` VALUES ('1', 'admin', '管理员');
INSERT INTO `role` VALUES ('2', 'user', '普通用户');

-- ----------------------------
-- Table structure for `role_privilege`
-- ----------------------------
DROP TABLE IF EXISTS `role_privilege`;
CREATE TABLE `role_privilege` (
  `roleId` int(11) NOT NULL,
  `privilegeId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`privilegeId`),
  UNIQUE KEY `privilegeId` (`roleId`,`privilegeId`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

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
INSERT INTO `role_privilege` VALUES ('2', '39');
INSERT INTO `role_privilege` VALUES ('2', '51');

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
INSERT INTO `user` VALUES ('71', 'admin1', '596450a3c03649219943179371616d7b', '221', '34234@123.com', '2', null, '12313', '1');
INSERT INTO `user` VALUES ('72', 'admin2', '885ee4b6ee92fc9aba945f2641fa3eca', 'admin23666', 'admin2@sunksisen.com', '2', '2020-01-02', 'nosession', '1');
INSERT INTO `user` VALUES ('73', 'admin3', '32cacb2f994f6b42183a1300d9a3e8d6', 'admin3', 'admin3@123.com', '2', '2020-01-03', 'no', '1');
INSERT INTO `user` VALUES ('74', 'admin4', 'fc1ebc848e31e0a68e868432225e3c82', 'admin4', 'admin4@123.com', '2', null, '', '1');
INSERT INTO `user` VALUES ('75', 'admin5', '26a91342190d515231d7238b0c5438e1', 'admin5', 'admin5@123.com', '2', '2020-01-05', '', '1');
INSERT INTO `user` VALUES ('76', 'test11', 'f696282aa4cd4f614aa995190cf442fe', 'test11', 'test11@123.com', '2', '2020-05-30', 'ss', '1');
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
