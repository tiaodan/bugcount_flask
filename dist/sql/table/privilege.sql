/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : hahahh

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2020-09-24 11:39:56
*/

SET FOREIGN_KEY_CHECKS=0;

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
