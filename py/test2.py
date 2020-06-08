from py import utils
# from py import buglist
# insert_passwd_sql = 'insert into bugcount.user values(null, %s, %s, null, null, null, null, null)'
# insert_passwd_sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user where username=%s'
# insert_passwd_sql = 'select *  from bugcount.user where username=%s'
# insert_passwd_sql = 'insert into bugcount.user values(null, %s, %s, null, null, null, null, null)'

# username_front = 'admin18'
# md5_passwd = 'admin18'
# dbutils.register(insert_passwd_sql, username_front, md5_passwd)
# dbutils.register(insert_passwd_sql, username_front, md5_passwd)
# dbutils.register(insert_passwd_sql, username_front, md5_passwd)

# dbutils.register(insert_passwd_sql)

# c_account.login(username_front, md5_passwd)
# username, password, user_remark, user_email, user_level, create_time, session
# admin.add_user(username_front, md5_passwd, '', '', 1, '2020-01-01', '')
# admin.add_user(username_front, md5_passwd, None, None, None, None, '')
# buglist.get_bugcount_by_project_orderby_time('2020-01-10', '2020-01-24')
# buglist.get_bugcount_by_project_orderby_time('2020-01-10', '2020-01-20')

# 测试获取配置文件所有键值对
# utils.get_dbargs_from_config()

# print(return_dict['db_host'])
# print(type(return_dict))


# buglist.get_allprojectdata_withproject_orderby_date('2020-01-10', '2020-01-20')
# buglist.get_allprojectdata_withproject_orderby_date('2020-01-10', '2020-01-20')
# buglist.get_allprojectdata_withproject_orderby_date()


# 读取配置文件
utils.get_dbargs_from_config()
# buglist.get_allprojectdata_withproject_orderby_date('2020-01-10', '2020-01-20')


