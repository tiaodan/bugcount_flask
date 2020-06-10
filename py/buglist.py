"""
管理buglist：
增删改查


"""

import pymysql
import json
#  引入python中的traceback模块，跟踪错误
import traceback
from py import utils

# 数据库配置
db_config_dict = utils.get_dbargs_from_config()

db_host = db_config_dict['db_host']
db_user = db_config_dict['db_user']
db_passwd = db_config_dict['db_passwd']
db_dbname = db_config_dict['db_dbname']
"""
db_host = 'localhost'
db_user = 'root'
db_passwd = 'sunkaisens'
db_dbname = 'bugcount'
"""

# 查询所有bug
# page = 当前页码，limit=当前页码显示个数
def search_buglist(page, limit):

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    buglist = []

    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user limit %s,%s'
        sql = 'select bugid, bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark, second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark, third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark from bugcount.buglist limit %s,%s'

        print(f'sql语句为==', sql)
        print(f'sql语句参数 *args====  page={page},limit={limit}')

        # print('sql语句参数args类型=={args}', type(args))

        # 执行sql语句
        begin_num = limit * (page - 1)
        print("《dbutil》 传的参数类型 ", type(begin_num), type(limit), begin_num, limit)

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        cursor.execute(sql, [begin_num, limit])
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        #转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        for r in sql_return_result_tuple:

            bug = dict()
            bug['bugid'] = r[0]
            bug['bug_submit_date'] = str(r[1])  # 转成str，否则会报TypeError: Object of type datetime is not JSON serializable
            bug['project'] = r[2]
            bug['software'] = r[3]
            bug['test_version'] = r[4]
            bug['bug_description'] = r[5]
            bug['severity_level'] = r[6] # 转成int 否则报错TypeError: not all arguments converted during string formatting
            bug['priority'] = r[7]
            bug['bug_difficulty'] = r[8]
            bug['bug_status'] = r[9]
            bug['bug_close_date'] = str(r[10])
            bug['close_version'] = r[11]
            bug['cause_analysis'] = r[12]
            bug['bug_img'] = r[13]
            bug['intermediate_situation'] = r[14]
            bug['developer'] = r[15]
            bug['remark'] = r[16]
            bug['first_bug_regression_date'] = str(r[17])
            bug['first_bug_regression_status'] = r[18]
            bug['first_bug_regression_remark'] = r[19]
            bug['second_bug_regression_date'] = str(r[20])
            bug['second_bug_regression_status'] = r[21]
            bug['second_bug_regression_remark'] = r[22]
            bug['third_bug_regression_date'] = str(r[23])
            bug['third_bug_regression_status'] = r[24]
            bug['third_bug_regression_remark'] = r[25]
            print('==============循环person==', bug)

            buglist.append(bug)
        print('????dbutil 转换完的【{}】格式数据users==', buglist)

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = '查询语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 编辑bug
def edit_bug(*args):

    # json数据
    data = {}
    buglist = []

    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:

        # sql = 'update bugcount.user set username=%s, password=%s, user_remark=%s, user_email=%s, user_level=%s, create_time=%s, session=%s where userid=%s'
        sql = 'update bugcount.buglist set bug_submit_date=%s, project=%s, software=%s, test_version=%s, bug_description=%s, severity_level=%s, priority=%s, bug_difficulty=%s, bug_status=%s, bug_close_date=%s, close_version=%s, cause_analysis=%s, bug_img=%s, intermediate_situation=%s, developer=%s, remark=%s, first_bug_regression_date=%s, first_bug_regression_status=%s, first_bug_regression_remark=%s, second_bug_regression_date=%s, second_bug_regression_status=%s, second_bug_regression_remark=%s, third_bug_regression_date=%s, third_bug_regression_status=%s, third_bug_regression_remark=%s where bugid=%s'
        print(f'sql语句为==', sql)
        print('sql语句参数 *args==== }', args)
        print('sql语句参数 *args type==== }', type(args))
        # print(f'完整的sqlw为 ：update bugcount.user set username={args[1]}, password={args[2]}, user_remark={args[3]}, user_email={args[4]}, user_level={args[5]}, create_time={args[6]}, session={args[7]} where userid={args[0]}')

        # userid, username, password, user_remark, user_email, user_level, create_time, session
        # print('sql语句参数args类型=={args}', type(args))

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        # 判断传入的日期参数 ，如果是空的话，不给sql语句传值就可以了，但是args是tuple类型，不支持删除--》转成list，将time替换成None

        args_list = list(args)  # tuple --> list
        if args[1] == '' or args[1] == 'None':
            print('将time赋值None')
            args_list[1] = None  # 转成None
        if args[10] == '' or args[10] == 'None':
            print('将time赋值None')
            args_list[10] = None  # 转成None
        if args[17] == '' or args[17] == 'None':
            print('将time赋值None')
            args_list[17] = None  # 转成None
        if args[20] == '' or args[20] == 'None':
            print('将time赋值None')
            args_list[20] = None  # 转成None
        if args[23] == '' or args[23] == 'None':
            print('将time赋值None')
            args_list[23] = None  # 转成None
        
        args = tuple(args_list) # list --> tuple


        # 多参数，execute要传2个参数，sql 和args分解出来的
        print('type(args)===================================', type(args))
        # cursor.execute(sql, args)  # 偶尔不好用
        args_test = [args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10]
                    , args[11], args[12], args[13], args[14], args[15], args[16], args[17], args[18], args[19], args[20]
                    , args[21], args[22], args[23], args[24], args[25], args[0]]  # 测试用
        cursor.execute(sql, args_test)  #  测试 用
        print('type(args_test)===================================', type(args_test))
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        # 转化下查询结果为{},{},{}这种格式======================
        print('????????result=', sql_return_result_tuple)
        print('????????????????????type = ', type(sql_return_result_tuple))

        for r in sql_return_result_tuple:
            bug = dict()
            bug['bugid'] = r[0]
            bug['bug_submit_date'] = str(r[1])  # 转成str，否则会报TypeError: Object of type datetime is not JSON serializable
            bug['project'] = r[2]
            bug['software'] = r[3]
            bug['test_version'] = r[4]
            bug['bug_description'] = r[5]
            bug['severity_level'] = r[6]
            bug['priority'] = r[7]
            bug['bug_difficulty'] = r[8]
            bug['bug_status'] = r[9]
            bug['bug_close_date'] = str(r[10])
            bug['close_version'] = r[11]
            bug['cause_analysis'] = r[12]
            bug['bug_img'] = r[13]
            bug['intermediate_situation'] = r[14]
            bug['developer'] = r[15]
            bug['remark'] = r[16]
            bug['first_bug_regression_date'] = str(r[17])
            bug['first_bug_regression_status'] = r[18]
            bug['first_bug_regression_remark'] = r[19]
            bug['second_bug_regression_date'] = str(r[20])
            bug['second_bug_regression_status'] = r[21]
            bug['second_bug_regression_remark'] = r[22]
            bug['third_bug_regression_date'] = str(r[23])
            bug['third_bug_regression_status'] = r[24]
            bug['third_bug_regression_remark'] = r[25]

            buglist.append(bug)
        print('????dbutil 转换完的【{}】格式数据users==', buglist)

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = 'edit user语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 删除bug
def del_bug(bugid):

    # json数据
    data = {}
    buglist = []

    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # 使用 execute()  方法执行 SQL 查询
    try:

        sql = 'delete from  bugcount.buglist where bugid = %s'
        print(f'sql语句为==', sql)
        print('sql语句参数 *args==== }', bugid)
        print('sql语句参数 *args type==== }', type(bugid))

        cursor.execute(sql, bugid)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'delbug语句执行成功'
        count = len(sql_return_result_tuple)  # sql语句结果个数

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 删除数据表 buglist
def truncate_table_buglist():

    # json数据
    data = {}
    buglist = []

    # 默认定义数据
    code = 500  # 默认失败
    msg = '清空数据表 buglist sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # 使用 execute()  方法执行 SQL 查询
    try:

        sql = 'truncate table bugcount.buglist'
        print(f'sql语句为==', sql)

        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("清空数据表 buglist  sql语句执行成功")

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = '清空数据表 buglist 语句执行成功'
        count = len(sql_return_result_tuple)  # sql语句结果个数

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 25个参数
def add_bug(*args):
    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    # json数据
    data = {}
    buglist = []

    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 默认bugid 是null 就按顺序加入mysql
        sql = 'insert into bugcount.buglist (bug_submit_date, project, software, test_version,' \
                                        ' bug_description, severity_level, priority, bug_difficulty, bug_status,' \
                                        ' bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation,' \
                                        ' developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark,' \
                                        ' second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark,' \
                                        ' third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark) ' \
              ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'


        print(f'sql语句为==', sql)
        print('sql语句参数 *args==== }', args)
        num = 0
        for i in args:
            print(f'sql语句参数 *args{num} type==== ', type(args[num]))
            num += 1
            if num == 25:
                break

        print('sql语句参数 *args type==== }', type(args))




        # username, password, user_remark, user_email, user_level, create_time, session
        # print('sql语句参数args类型=={args}', type(args))

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        # 判断传入的日期参数 ，如果是空的话，不给sql语句传值就可以了，但是args是tuple类型，不支持删除--》转成list，将time替换成None
        args_list = list(args)  # tuple --> list
        if args[1] == '' or args[1] == 'None':
            print('将time赋值None')
            args_list[1] = '0000-00-00'  # 转成None
            print('args_list[1] = ', args_list[1])
        if args[10] == '' or args[10] == 'None':
            print('将time赋值None')
            # args_list[10] = None  # 转成None
            args_list[10] = '0000-00-00'  # 转成None
            print('args_list[1] = ', args_list[10])
        if args[17] == '' or args[17] == 'None':
            print('将time赋值None')
            args_list[17] = '0000-00-00'  # 转成None
            print('args_list[1] = ', args_list[17])
        if args[20] == '' or args[20] == 'None':
            print('将time赋值None')
            args_list[20] = '0000-00-00'  # 转成None
            print('args_list[1] = ', args_list[20])
        if args[23] == '' or args[23] == 'None':
            print('将time赋值None')
            args_list[23] = '0000-00-00'  # 转成None
            print('args_list[1] = ', args_list[23])

        # """
        #     后台统一转换参数格式，处理"" 或者NaN情况
        num = 0
        for i in args_list:
            if args_list[num] == 'NaN':
                args_list[num] = None
                num += 1
        num = 0
        # """
        print('sql语句参数 转换后  *args==== }', args)

        args = tuple(args_list)  # list --> tuple

        # 多参数，execute要传2个参数，sql 和args分解出来的
        print('type(args)===================================', type(args))
        # cursor.execute(sql, args)  # 偶尔不好用
        args_test = [args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10]
            , args[11], args[12], args[13], args[14], args[15], args[16], args[17], args[18], args[19], args[20]
            , args[21], args[22], args[23], args[24]]  # 测试用

        print("打印  tuple类型的参数 ", len(args_test))



        cursor.execute(sql, args_test)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        # 转化下查询结果为{},{},{}这种格式======================
        print('????????result=', sql_return_result_tuple)
        print('????????????????????type = ', type(sql_return_result_tuple))

        for r in sql_return_result_tuple:

            bug = dict()
            # 没有bugid
            bug['bug_submit_date'] = str(r[0])  # 转成str，否则会报TypeError: Object of type datetime is not JSON serializable
            bug['project'] = r[1]
            bug['software'] = r[2]
            bug['test_version'] = r[3]
            bug['bug_description'] = r[4]
            bug['severity_level'] = r[5]
            bug['priority'] = r[6]
            bug['bug_difficulty'] = r[7]
            bug['bug_status'] = r[8]
            bug['bug_close_date'] = str(r[9])
            bug['close_version'] = r[10]
            bug['cause_analysis'] = r[11]
            bug['bug_img'] = r[12]
            bug['intermediate_situation'] = r[13]
            bug['developer'] = r[14]
            bug['remark'] = r[15]
            bug['first_bug_regression_date'] = str(r[16])
            bug['first_bug_regression_status'] = r[17]
            bug['first_bug_regression_remark'] = r[18]
            bug['second_bug_regression_date'] = str(r[19])
            bug['second_bug_regression_status'] = r[20]
            bug['second_bug_regression_remark'] = r[21]
            bug['third_bug_regression_date'] = str(r[22])
            bug['third_bug_regression_status'] = r[23]
            bug['third_bug_regression_remark'] = r[24]

            buglist.append(bug)
            print('????dbutil 转换完的【{}】格式数据users==', buglist)

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = 'add bug语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 获取bug统计信息- 项目维度
def get_bugcount_by_project(startTime, endTime):

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    bugcount = []

    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 所有项目

        # sql = "select project,count(bug_status = 1 or null) as 'add', count(bug_status = 2 or null) as 'close',count(bug_status = 3 or null) as 'regression',count(bug_status = 4 or null) as 'delay', count(bug_status = 1 and severity_level <= 2 or null) as 'add12', count(bug_status = 2 and severity_level <= 2 or null) as 'close12', count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', count(severity_level <= 2 or null) as 'delay12', convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', count(bugid or null) as 'totalNum' from bugcount.buglist where (bug_submit_date >= '2020-01-10' and  bug_submit_date <= '2020-01-24' ) group by project;"
        sql = "select bug_submit_date, project,count(bug_status = 1 or null) as 'add', " \
              "count(bug_status = 2 or null) as 'close'," \
              "count(bug_status = 3 or null) as 'regression', " \
              "count(bug_status = 4 or null) as 'delay', " \
              "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
              "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
              "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
              "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
              "count(severity_level <= 2 or null) as 'delay12', " \
              "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
              "count(bugid or null) as 'totalNum' from bugcount.buglist " \
              "where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by project order by rate desc;"

        print(f'sql语句为==', sql)
        print('sql语句参数starTime,end Time =={args}', startTime, endTime)

        # 执行sql语句

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        cursor.execute(sql, [startTime, endTime])
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        #转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        rank = 1
        for r in sql_return_result_tuple:
            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['project'] = r[1]  # 项目名称
            bug['addNumByProject'] = r[2]  # 新增
            bug['closeNumByProject'] = r[3]  # 关闭
            bug['regressionNumByProject'] = r[4]  # 回归
            bug['delayNumByProject'] = r[5]  # 延迟
            bug['addLeve12NumByProject'] = r[6]  # 12级bug新增
            bug['closeLevel12NumByProject'] = r[7]  # 1-2级bug关闭
            bug['regressionLeve12NumByProject'] = r[8]  # 1-2级bug回归
            bug['delayLeve12NumByProject'] = r[9]  # 1-2级bug延迟
            bug['totalLevel12NumByProject'] = r[10]  # 1-2级bug总数
            bug['bugCloseRateByProject'] = float(r[11])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rankByProjectByProject'] = rank  #排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1
            bug['totalNumByProject'] = r[12]  # 总数
            rank += 1
            print('==============循环person==', bug)

            bugcount.append(bug)
        print('????dbutil 转换完的【{}】格式数据users==', bugcount)

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = '查询语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 获取bug统计信息- 项目维度 - 用来画折线图
def get_bugcount_by_project_orderby_time_error_nouse(startTime, endTime):

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    bugcount = []

    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个project
        get_project_sql = 'select project from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by project'
        cursor.execute(get_project_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        project_tuple = cursor.fetchall()

        # 获取有多少日期
        get_date_sql = 'select bug_submit_date from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )  group by bug_submit_date order by bug_submit_date'
        cursor.execute(get_date_sql, [startTime, endTime])
        conn.commit()
        date_tuple = cursor.fetchall()

        # 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project,count(bug_status = 1 or null) as 'add', " \
                                  "count(bug_status = 2 or null) as 'close'," \
                                  "count(bug_status = 3 or null) as 'regression', " \
                                  "count(bug_status = 4 or null) as 'delay', " \
                                  "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
                                  "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                  "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                  "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                  "count(severity_level <= 2 or null) as 'total12', " \
                                  "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                  "count(bugid or null) as 'totalNum' "

        searchsql_end =  " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by bug_submit_date order by bug_submit_date"
        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        search_sql_args = list()


        fornum = 0   #sql for下标
        for i in project_tuple:
            print(f'当前第{fornum}项 循环：第{fornum}项目为', i, project_tuple[fornum])
            print('项目有：', project_tuple)
            print('项目 长度len(project_tuple)====', len(project_tuple))
            print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug
            sql_total_num_byproject_belong_project0 = ",count(project=%s or null) as %s "
            sql_add_num_byproject_belong_project0 = ",count(bug_status=1 and project = %s or null) as %s "
            sql_close_num_byproject_belong_project0 = ",count(bug_status=2 and project = %s or null) as %s "

            #拼接
            searchsql_not_complete += sql_total_num_byproject_belong_project0
            searchsql_not_complete += sql_add_num_byproject_belong_project0
            searchsql_not_complete += sql_close_num_byproject_belong_project0

            #给 sql参数赋值 - 6个参数
                # 依次为属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug


            sqlarg_total_project0_name = project_tuple[fornum]  # 1808
            sqlarg_total_project0_name_aS = "totalNumByProjectBelongProject" + str(fornum)  # totalNumByProjectBelongProject0
            print('???sqlarg_total_project0_name, sqlarg_total_project0_name_aS ====', sqlarg_total_project0_name, sqlarg_total_project0_name_aS)
            sqlarg_add_project0_name = project_tuple[fornum]  # 1808
            sqlarg_add_project0_name_aS = "addNumByProjectBelongProject" + str(fornum)  # totalNumByProjectBelongProject0
            sqlarg_close_project0_name = project_tuple[fornum]  # 1808
            sqlarg_close_project0_name_aS = "closeNumByProjectBelongProject" + str(fornum)  # totalNumByProjectBelongProject0
            fornum += 1

            # 将参数依次添加进去
            search_sql_args.append(sqlarg_total_project0_name)
            search_sql_args.append(sqlarg_total_project0_name_aS)
            search_sql_args.append(sqlarg_add_project0_name)
            search_sql_args.append(sqlarg_add_project0_name_aS)
            search_sql_args.append(sqlarg_close_project0_name)
            search_sql_args.append(sqlarg_close_project0_name_aS)
            print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

        #     最终sql
        search_sql = searchsql_not_complete + searchsql_end
        print("《查询项目折线图 - 统计数据 - sql = 》", search_sql)

        # sql参数 + 起始终止时间
        search_sql_args.append(startTime)
        search_sql_args.append(endTime)
        print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

        # 执行sql语句
        cursor.execute(search_sql, search_sql_args)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        #转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")


        bug = dict()
        # 给需要累加的 赋初始值
        forum_project = 0
        for i in sql_return_result_tuple:
            bug['totalNumByProjectBelongProjectSum' + str(forum_project)] = 0
            bug['addNumByProjectBelongProjectSum' + str(forum_project)] = 0
            bug['closeNumByProjectBelongProjectSum' + str(forum_project)] = 0
            forum_project += 1

        rank = 1

        print('?????????????????? sql_return_result_tuple 时间==', sql_return_result_tuple[0])
        print('?????????????????? sql_return_result_tuple 时间 type ==', type(sql_return_result_tuple[0]))

        forum_project = 0 # 重新赋值0，给下一个循环用
        for r in sql_return_result_tuple:
        # for r in date_tuple:

            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            date = str(r[0])
            bug['project'] = r[1]  # 项目名称
            bug['addNumByProject'] = r[2]  # 新增
            bug['closeNumByProject'] = r[3]  # 关闭
            bug['regressionNumByProject'] = r[4]  # 回归
            bug['delayNumByProject'] = r[5]  # 延迟
            bug['addLeve12NumByProject'] = r[6]  # 12级bug新增
            bug['closeLevel12NumByProject'] = r[7]  # 1-2级bug关闭
            bug['regressionLeve12NumByProject'] = r[8]  # 1-2级bug回归
            bug['delayLeve12NumByProject'] = r[9]  # 1-2级bug延迟
            bug['totalLevel12NumByProject'] = r[10]  # 1-2级bug总数
            bug['bugCloseRateByProject'] = float(r[11])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rankByProjectByProject'] = rank  #排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1
            bug['totalNumByProject'] = r[12]  # 总数
            # bug['totalNumByProjectBelongProject0'] = r[13]  # 总数
            # """
            bug['totalNumByProjectBelongProject' + str(forum_project)] = r[13 + forum_project]  # 属于项目0的全部bug
            print('????????????????????????????????????r[13 + fornum] =========', r[13 + fornum])
            bug['addNumByProjectBelongProject' + str(forum_project)] = r[13 + forum_project]  # 属于项目0的新增bug
            bug['closeNumByProjectBelongProject' + str(forum_project)] = r[13 + forum_project]  # 属于项目0的关闭bug
            # """
            #取值： 属于项目0的全部bug / 属于项目0的新增bug / 属于项目0的关闭bug
                #要取值的是每一天的累加数量，在此进行累加
            # """
            """
                        这种格式的
                        bug_submit_date | project | add | close | regression | delay | add12 | close12 | regression12 | delay12 | bugNum12 | rate | totalNum | totalNumByProjectBelongProject0 | addNumByProjectBelongProject0 | closeNumByProjectBelongProject0 |
                        +-----------------+---------+-----+-------+------------+-------+-------+---------+--------------+---------+----------+------+----------+---------------------------------+-------------------------------+---------------------------------+
                        | 2020-01-23      | 1808    |   1 |     0 |          1 |     0 |     0 |       0 |            0 |       0 |        0 | 0    |        2 |                      （累加） 1 |                （累加)      1 |                     （累加）  0 |
                        | 2020-01-24      | 1808    |   1 |     1 |          0 |     0 |     0 |       0 |            0 |       0 |        0 | 0.5  |        2 |                               1 |                             1 |                               0 |

            """
            for project_num in date_tuple:
                bug['totalNumByProjectBelongProjectSum' + str(forum_project)] += r[13 + forum_project * 3]  # 属于项目0的全部bug
                bug['addNumByProjectBelongProjectSum' + str(forum_project)] += r[13 + forum_project * 3 + 1]  # 属于项目0的新增bug
                bug['closeNumByProjectBelongProjectSum' + str(forum_project)] += r[13 + forum_project * 3 + 2]  # 属于项目0的关闭bug

                print(f'????????? 第{forum_project}次循环，日期{date}---- 前后对比 bug总数（前，后），新增总数（前，后）， 关闭总数（前后） =========',
                      r[13 + forum_project * 3], bug['totalNumByProjectBelongProjectSum' + str(forum_project)],
                      r[13 + forum_project * 3 + 1], bug['addNumByProjectBelongProjectSum' + str(forum_project)],
                      r[13 + forum_project * 3 + 2], bug['closeNumByProjectBelongProjectSum' + str(forum_project)]
                      )

            rank += 1
            print('==============循环person==', bug)

            forum_project += 1

            bugcount.append(bug)  # 装的是每天的数量
        # for 循环添加data 完成

        print('????dbutil 转换完的【{}】格式数据users==', bugcount)


        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = '查询语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)

    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str

# 获取bug统计信息- 项目维度 - 用来画折线图
def get_bugcount_by_project_orderby_time(startTime, endTime):

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    bugcount = []

    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个project
        get_project_sql = 'select project from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by project'
        cursor.execute(get_project_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        project_tuple = cursor.fetchall()


        # 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project,count(bug_status = 1 or null) as 'add', " \
                                  "count(bug_status = 2 or null) as 'close'," \
                                  "count(bug_status = 3 or null) as 'regression', " \
                                  "count(bug_status = 4 or null) as 'delay', " \
                                  "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
                                  "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                  "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                  "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                  "count(severity_level <= 2 or null) as 'delay12', " \
                                  "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                  "count(bugid or null) as 'totalNum' "

        searchsql_end =  " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by bug_submit_date order by bug_submit_date"
        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        search_sql_args = list()


        fornum = 0   #sql for下标
        for i in project_tuple:
            print(f'当前第{fornum}项 循环：第{fornum}项目为', i, project_tuple[fornum])
            print('项目有：', project_tuple)
            print('项目 长度len(project_tuple)====', len(project_tuple))
            print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug
            sql_total_num_byproject_belong_project0 = ",count(project=%s or null) as %s "
            sql_add_num_byproject_belong_project0 = ",count(bug_status=1 and project = %s or null) as %s "
            sql_close_num_byproject_belong_project0 = ",count(bug_status=2 and project = %s or null) as %s "

            #拼接
            searchsql_not_complete += sql_total_num_byproject_belong_project0
            searchsql_not_complete += sql_add_num_byproject_belong_project0
            searchsql_not_complete += sql_close_num_byproject_belong_project0

            #给 sql参数赋值 - 6个参数
                # 依次为属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug


            sqlarg_total_project0_name = project_tuple[fornum]  # 1808
            sqlarg_total_project0_name_aS = "totalNumByProjectBelongProject" + str(fornum)  # totalNumByProjectBelongProject0
            print('???sqlarg_total_project0_name, sqlarg_total_project0_name_aS ====', sqlarg_total_project0_name, sqlarg_total_project0_name_aS)
            sqlarg_add_project0_name = project_tuple[fornum]  # 1808
            sqlarg_add_project0_name_aS = "addNumByProjectBelongProject" + str(fornum)  # totalNumByProjectBelongProject0
            sqlarg_close_project0_name = project_tuple[fornum]  # 1808
            sqlarg_close_project0_name_aS = "closeNumByProjectBelongProject" + str(fornum)  # totalNumByProjectBelongProject0
            fornum += 1

            # 将参数依次添加进去
            search_sql_args.append(sqlarg_total_project0_name)
            search_sql_args.append(sqlarg_total_project0_name_aS)
            search_sql_args.append(sqlarg_add_project0_name)
            search_sql_args.append(sqlarg_add_project0_name_aS)
            search_sql_args.append(sqlarg_close_project0_name)
            search_sql_args.append(sqlarg_close_project0_name_aS)
            print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

        #     最终sql
        search_sql = searchsql_not_complete + searchsql_end
        print("《查询项目折线图 - 统计数据 - sql = 》", search_sql)

        # sql参数 + 起始终止时间
        search_sql_args.append(startTime)
        search_sql_args.append(endTime)
        print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

        # 执行sql语句
        cursor.execute(search_sql, search_sql_args)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        #转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        rank = 1

        for_num_project = 0  # 重新赋值0，给下一个循环用
        for r in sql_return_result_tuple:
            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            date = str(r[0])
            bug['project'] = r[1]  # 项目名称
            bug['addNumByProject'] = r[2]  # 新增
            bug['closeNumByProject'] = r[3]  # 关闭
            bug['regressionNumByProject'] = r[4]  # 回归
            bug['delayNumByProject'] = r[5]  # 延迟
            bug['addLeve12NumByProject'] = r[6]  # 12级bug新增
            bug['closeLevel12NumByProject'] = r[7]  # 1-2级bug关闭
            bug['regressionLeve12NumByProject'] = r[8]  # 1-2级bug回归
            bug['delayLeve12NumByProject'] = r[9]  # 1-2级bug延迟
            bug['totalLevel12NumByProject'] = r[10]  # 1-2级bug总数
            bug['bugCloseRateByProject'] = float(r[11])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rankByProjectByProject'] = rank  #排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1
            bug['totalNumByProject'] = r[12]  # 总数
            # bug['totalNumByProjectBelongProject0'] = r[13]  # 总数

            for i in project_tuple:
                bug['totalNumByProjectBelongProject' + str(for_num_project)] = r[13 + for_num_project *3]  # 属于项目0的全部bug
                # print(f'?????????????? total Bug project{project_tuple} ??????????????r[13 + for_num_project] =========', r[13 + for_num_project *3])
                print('?????????????? total Bug project{0} ??????????????r[13 + for_num_project] =========', r[13])
                bug['addNumByProjectBelongProject' + str(for_num_project)] = r[13 + for_num_project*3 +1]  # 属于项目0的新增bug
                bug['closeNumByProjectBelongProject' + str(for_num_project)] = r[13 + for_num_project*3 +2]  # 属于项目0的关闭bug
                for_num_project += 1


            #取值： 属于项目0的全部bug / 属于项目0的新增bug / 属于项目0的关闭bug


            """
                        这种格式的
                        bug_submit_date | project | add | close | regression | delay | add12 | close12 | regression12 | delay12 | bugNum12 | rate | totalNum | totalNumByProjectBelongProject0 | addNumByProjectBelongProject0 | closeNumByProjectBelongProject0 |
                        +-----------------+---------+-----+-------+------------+-------+-------+---------+--------------+---------+----------+------+----------+---------------------------------+-------------------------------+---------------------------------+
                        | 2020-01-23      | 1808    |   1 |     0 |          1 |     0 |     0 |       0 |            0 |       0 |        0 | 0    |        2 |                      （累加） 1 |                （累加)      1 |                     （累加）  0 |
                        | 2020-01-24      | 1808    |   1 |     1 |          0 |     0 |     0 |       0 |            0 |       0 |        0 | 0.5  |        2 |                               1 |                             1 |                               0 |

            """

            rank += 1
            print('==============循环person==', bug)

            bugcount.append(bug)  # 装的是每天的数量
        # for 循环添加data 完成

        print('????dbutil 转换完的【{}】格式数据users==', bugcount)


        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = '查询语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)

    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str


# 获取bug统计信息- 开发维度 -- 用来填充 统计界面的表格
def get_bugcount_by_developer(startTime, endTime):

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    bugcount = []

    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 所有项目

        # sql = "select project,count(bug_status = 1 or null) as 'add', count(bug_status = 2 or null) as 'close',count(bug_status = 3 or null) as 'regression',count(bug_status = 4 or null) as 'delay', count(bug_status = 1 and severity_level <= 2 or null) as 'add12', count(bug_status = 2 and severity_level <= 2 or null) as 'close12', count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', count(severity_level <= 2 or null) as 'delay12', convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', count(bugid or null) as 'totalNum' from bugcount.buglist where (bug_submit_date >= '2020-01-10' and  bug_submit_date <= '2020-01-24' ) group by project;"
        sql = "select bug_submit_date, developer, count(bug_status = 1 or null) as 'add', " \
              "count(bug_status = 2 or null) as 'close'," \
              "count(bug_status = 3 or null) as 'regression', " \
              "count(bug_status = 4 or null) as 'delay', " \
              "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
              "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
              "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
              "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
              "count(severity_level <= 2 or null) as 'delay12', " \
              "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
              "count(bugid or null) as 'totalNum' from bugcount.buglist " \
              "where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by developer order by rate desc;"

        print(f'sql语句为==', sql)
        print('sql语句参数starTime,end Time =={args}', startTime, endTime)

        # 执行sql语句

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        cursor.execute(sql, [startTime, endTime])
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        #转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        rank = 1
        for r in sql_return_result_tuple:
            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['developer'] = r[1]  # 项目名称
            bug['addNumByDeveloper'] = r[2]  # 新增
            bug['closeNumByDeveloper'] = r[3]  # 关闭
            bug['regressionNumByDeveloper'] = r[4]  # 回归
            bug['delayNumByDeveloper'] = r[5]  # 延迟
            bug['addLeve12NumByDeveloper'] = r[6]  # 12级bug新增
            bug['closeLevel12NumByDeveloper'] = r[7]  # 1-2级bug关闭
            bug['regressionLeve12NumByDeveloper'] = r[8]  # 1-2级bug回归
            bug['delayLeve12NumByDeveloper'] = r[9]  # 1-2级bug延迟
            bug['totalLevel12NumByDeveloper'] = r[10]  # 1-2级bug总数
            bug['bugCloseRateByDeveloper'] = float(r[11])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rankByProjectByDeveloper'] = rank  #排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1
            bug['totalNumByDeveloper'] = r[12]  # 总数
            rank += 1
            print('==============循环person==', bug)

            bugcount.append(bug)
        print('????dbutil 转换完的【{}】格式数据users==', bugcount)

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = '查询语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str



"""
                 这种格式的
                 bug_submit_date | project | add | close | regression | delay | add12 | close12 | regression12 | delay12 | bugNum12 | rate | totalNum | totalNumByProjectBelongProject0 | addNumByProjectBelongProject0 | closeNumByProjectBelongProject0 |
                 +-----------------+---------+-----+-------+------------+-------+-------+---------+--------------+---------+----------+------+----------+---------------------------------+-------------------------------+---------------------------------+
                 | 2020-01-23      | 1808    |   1 |     0 |          1 |     0 |     0 |       0 |            0 |       0 |        0 | 0    |        2 |                      （累加） 1 |                （累加)      1 |                     （累加）  0 |
                 | 2020-01-24      | 1808    |   1 |     1 |          0 |     0 |     0 |       0 |            0 |       0 |        0 | 0.5  |        2 |                               1 |                             1 |                               0 |

"""
# 获取所有项目的数据，为了画折线图project0 - project13(默认给13个项目，没有值默认不返回数据, ！！ 有几个项目返回几个项目的值)
def get_allprojectdata_withproject_orderby_date(startTime, endTime):
    print('=================================获取所有项目的数据 start ===================================')
    print(f'app.py 传的参数{startTime}， {endTime}')

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    bugcount = []
    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数

        # 1. 获取有几个project
        get_project_sql = 'select project from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by project'
        cursor.execute(get_project_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        project_tuple = cursor.fetchall()


        print(f'1. 获取有多少项目==={project_tuple}')
        print(f'1. 获取 project_tuple type ==={type(project_tuple)}')
        print(f'1. 获取有多少项目 len===', len(project_tuple))
        print(f'1. project_tuplen===> list', list(project_tuple))
        print(f'1. project_tuplen===> list[0]', list(project_tuple)[0])
        print(f'1. project_tuplen===> tuple[0],结论 tuple[0]==list[0]', project_tuple[0])
        print(f'1. project_tuplen===> tuple[0] type', type(project_tuple[0]))
        str1808 = str(project_tuple[0])
        print(f'1. project_tuplen===> tuple[0] type tuple --> str', str1808)
        print(f'1. project_tuplen===> tuple[0] type str1808 --> str', type(str1808))
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取字符串（"1808",）', type(str1808))
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 字符串长度（"1808",）', len(str1808)) # 9位
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取（"1808",）', str1808[0])  # 9位
        # 0-len(str)-2
        ppname = str1808[1:len(str1808)-2]
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取（"1808",） 1-len(str)-2', ppname)

        """
        # 获取有多少日期
        get_date_sql = 'select bug_submit_date from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )  group by bug_submit_date order by bug_submit_date'
        cursor.execute(get_date_sql, [startTime, endTime])
        conn.commit()
        date_tuple = cursor.fetchall()
        """

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project,count(bug_status = 1 or null) as 'add', " \
                                  "count(bug_status = 2 or null) as 'close'," \
                                  "count(bug_status = 3 or null) as 'regression', " \
                                  "count(bug_status = 4 or null) as 'delay', " \
                                  "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
                                  "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                  "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                  "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                  "count(severity_level <= 2 or null) as 'delay12', " \
                                  "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                  "count(bugid or null) as 'totalNum' "

        searchsql_end =  " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by bug_submit_date order by bug_submit_date"
        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        search_sql_args = list()
        print('未拼接好的字符串==', searchsql_not_complete + searchsql_end)

        search_sql_middle_about_project = ""
        # 循环拼接字符串
        for project in project_tuple:
            # 当前索引
            print(f'当前project=={str(project)}')
            index = project_tuple.index(project)
            project_name_tuple_to_str = str(project_tuple[index])
            project_name = project_name_tuple_to_str[1:len(project_name_tuple_to_str)-2]
            print('循环中的项目名str==', project_name)


            print(f'当前第{index}项 循环：第{index}项目为', project_name)
            print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为项目1 / 属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug

            # project='1808' as project0
            sql_name_project = ",project=" + project_name + "as project" + str(index)
            print('name ==========', sql_name_project)

            sql_add_num_byproject_belong_project = ",count(bug_status=1 and project = " + project_name + "or null) as add_num_project" + str(index)
            sql_close_num_byproject_belong_project = ",count(bug_status=2 and project = " + project_name + "or null) as close_num_project" + str(index)
            sql_regression_num_byproject_belong_project = ",count(bug_status=3 and project = " + project_name + "or null) as regression_num_project" + str(index)
            sql_delay_num_byproject_belong_project = ",count(bug_status=4 and project = " + project_name + "or null) as delay_num_project" + str(index)
            print('for 循环拼接的sql == ', sql_name_project + sql_add_num_byproject_belong_project +sql_close_num_byproject_belong_project +
                  sql_regression_num_byproject_belong_project + sql_delay_num_byproject_belong_project)

            for_sql = sql_name_project + sql_add_num_byproject_belong_project +sql_close_num_byproject_belong_project + sql_regression_num_byproject_belong_project + sql_delay_num_byproject_belong_project
            # search_sql_middle_about_project 基础上拼接
            search_sql_middle_about_project += for_sql
            print('项目相关sql 拼接结果==', search_sql_middle_about_project)


        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_project + searchsql_end
        print('最终sql ==', search_sql)

        # 2. 执行sql语句
        cursor.execute(search_sql, [startTime, endTime])
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        rank = 1 # 排名
        # 3. 整理返回给前端的值,相当于按时间循环
            # 返回数据 第几行 第几列xx数据
        for r in sql_return_result_tuple:
            print('=======================r=', r)

            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            print('========================bug_submit_date', bug['bug_submit_date'])
            bug['project'] = r[1]  # 项目名称
            bug['add'] = r[2]  # 新增
            bug['close'] = r[3]  # 关闭
            bug['regression'] = r[4]  # 回归
            bug['delay'] = r[5]  # 延迟
            bug['add12'] = r[6]  # 12级bug新增
            bug['close12'] = r[7]  # 1-2级bug关闭
            bug['regression12'] = r[8]  # 1-2级bug回归
            bug['delay12'] = r[9]  # 1-2级bug延迟
            bug['total12'] = r[10]  # 1-2级bug总数
            bug['bugCloseRate'] = float(r[11])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rank'] = rank  # 排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1，不是从数据库查的，自己算的
            bug['totalNum'] = r[12]  # 总数

            # 后面是项目相关的 关闭情况，有几个项目循环几次
            for project in project_tuple:
                # 当前索引
                print(f'当前project=={str(project)}')
                index = project_tuple.index(project)
                print(f'当前索引=={index}')
                print(f'第{index}次循环开始================================================')

                # project0

                #   str1808[1:len(str1808)-2] 截取字符串 中project名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中project名字--》1808 (去掉''格式的)
                bug['project' + str(index)] = str(project)[2:len(str(project))-3]  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出
                bug['add_project' + str(index)] = r[13 + 5*index + 1]
                bug['close_project' + str(index)] = r[13 + 5*index + 2]
                bug['regression_project' + str(index)] = r[13 + 5*index + 3]
                bug['delay_project' + str(index)] = r[13 + 5*index + 4]

                print(f'project{index}=', bug['project' + str(index)])  #
                print(f'add_project{index}=', bug['add_project' + str(index)])
                print(f'close_project{index} ==', bug['close_project' + str(index)])
                print(f'regression_project{index}  ===', bug['regression_project' + str(index)])
                print(f'delay_project{index}  ===', bug['delay_project' + str(index)])

                print(f'第{index}次循环结束================================================')

            # 循环完1次 累加
            bugcount.append(bug)
            # for end

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 查询成功
        if count > 0:
            code = 200  # 成功
            msg = '查询语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist> 返回结果==jsonStr=====', json_str)


    print('=================================获取所有项目的数据 end ===================================')
    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str


# 获取所有项目的数据，为了画折线图project0 - project13(默认给13个开发，没有值默认不返回数据, ！！ 有几个项目返回几个项目的值)
def get_allprojectdata_withdeveoper_orderby_date(startTime, endTime):
    print('=================================获取所有 开发 的数据 start ===================================')
    print(f'app.py 传的参数{startTime}， {endTime}')

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    bugcount = []
    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数

        # 1. 获取有几个project
        get_developer_sql = 'select developer from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by developer'
        cursor.execute(get_developer_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        developer_tuple = cursor.fetchall()


        print(f'1. 获取有多少开发==={developer_tuple}')
        print(f'1. 获取 project_tuple type ==={type(developer_tuple)}')
        print(f'1. 获取有多少开发 len===', len(developer_tuple))
        print(f'1. project_tuplen===> list', list(developer_tuple))
        print(f'1. project_tuplen===> list[0]', list(developer_tuple)[0])
        print(f'1. project_tuplen===> tuple[0],结论 tuple[0]==list[0]', developer_tuple[0])
        print(f'1. project_tuplen===> tuple[0] type', type(developer_tuple[0]))
        str1808 = str(developer_tuple[0])
        print(f'1. project_tuplen===> tuple[0] type tuple --> str', str1808)
        print(f'1. project_tuplen===> tuple[0] type str1808 --> str', type(str1808))
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取字符串（"1808",）', type(str1808))
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 字符串长度（"1808",）', len(str1808)) # 9位
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取（"1808",）', str1808[0])  # 9位
        # 0-len(str)-2
        ppname = str1808[1:len(str1808)-2]
        print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取（"1808",） 1-len(str)-2', ppname)

        """
        # 获取有多少日期
        get_date_sql = 'select bug_submit_date from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )  group by bug_submit_date order by bug_submit_date'
        cursor.execute(get_date_sql, [startTime, endTime])
        conn.commit()
        date_tuple = cursor.fetchall()
        """

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project,count(bug_status = 1 or null) as 'add', " \
                                  "count(bug_status = 2 or null) as 'close'," \
                                  "count(bug_status = 3 or null) as 'regression', " \
                                  "count(bug_status = 4 or null) as 'delay', " \
                                  "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
                                  "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                  "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                  "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                  "count(severity_level <= 2 or null) as 'delay12', " \
                                  "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                  "count(bugid or null) as 'totalNum' "

        searchsql_end =  " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by bug_submit_date order by bug_submit_date"
        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        search_sql_args = list()
        print('未拼接好的字符串==', searchsql_not_complete + searchsql_end)

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            print(f'当前 developer =={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str)-2]
            print('循环中的 developer 名str==', developer_name)


            print(f'当前第{index}项 循环：第{index}项目为', developer_name)
            print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为开发1 / 属于开发1的全部bug / 属于开发1的新增bug / 属于开发1的关闭bug

            # project='1808' as project0
            sql_name_developer = ",developer=" + developer_name + " as developer" + str(index)
            print('name ==========', sql_name_developer)
            # 执行到这没问题

            sql_add_num_bydeveloper_belong_developer = ",count(bug_status=1 and developer = " + developer_name + " or null) as add_num_developer" + str(index)
            sql_close_num_bydeveloper_belong_developer = ",count(bug_status=2 and developer = " + developer_name + " or null) as close_num_developer" + str(index)
            sql_regression_num_bydeveloper_belong_developer = ",count(bug_status=3 and developer = " + developer_name + " or null) as regression_num_developer" + str(index)
            sql_delay_num_bydeveloper_belong_developer = ",count(bug_status=4 and developer = " + developer_name + " or null) as delay_num_developer" + str(index)
            print('for 循环拼接的sql == ', sql_name_developer + sql_add_num_bydeveloper_belong_developer +sql_close_num_bydeveloper_belong_developer +
                  sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer)

            for_sql = sql_name_developer + sql_add_num_bydeveloper_belong_developer +sql_close_num_bydeveloper_belong_developer + sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer
            print('for sql ======', for_sql)
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            print('开发相关sql 拼接结果==', search_sql_middle_about_developer)


        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_developer + searchsql_end
        print('最终sql ==', search_sql)

        # 2. 执行sql语句
        cursor.execute(search_sql, [startTime, endTime])
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        rank = 1 # 排名
        # 3. 整理返回给前端的值,相当于按时间循环
            # 返回数据 第几行 第几列xx数据
        for r in sql_return_result_tuple:
            print('=======================r=', r)

            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            print('========================bug_submit_date', bug['bug_submit_date'])
            bug['project'] = r[1]  # 项目名称
            bug['add'] = r[2]  # 新增
            bug['close'] = r[3]  # 关闭
            bug['regression'] = r[4]  # 回归
            bug['delay'] = r[5]  # 延迟
            bug['add12'] = r[6]  # 12级bug新增
            bug['close12'] = r[7]  # 1-2级bug关闭
            bug['regression12'] = r[8]  # 1-2级bug回归
            bug['delay12'] = r[9]  # 1-2级bug延迟
            bug['total12'] = r[10]  # 1-2级bug总数
            bug['bugCloseRate'] = float(r[11])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rank'] = rank  # 排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1，不是从数据库查的，自己算的
            bug['totalNum'] = r[12]  # 总数

            # 后面是项目相关的 关闭情况，有几个项目循环几次
            for developer in developer_tuple:
                # 当前索引
                print(f'当前developer=={str(developer)}')
                index = developer_tuple.index(developer)
                print(f'当前索引=={index}')
                print(f'第{index}次循环开始================================================')

                # project0

                #   str1808[1:len(str1808)-2] 截取字符串 中developer名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中developer名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer))-3]  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出
                bug['add_developer' + str(index)] = r[13 + 5*index + 1]
                bug['close_developer' + str(index)] = r[13 + 5*index + 2]
                bug['regression_developer' + str(index)] = r[13 + 5*index + 3]
                bug['delay_developer' + str(index)] = r[13 + 5*index + 4]

                print(f'developer{index}=', bug['developer' + str(index)])  #
                print(f'add_developer{index}=', bug['add_developer' + str(index)])
                print(f'close_developer{index} ==', bug['close_developer' + str(index)])
                print(f'regression_developer{index}  ===', bug['regression_developer' + str(index)])
                print(f'delay_developer{index}  ===', bug['delay_developer' + str(index)])

                print(f'第{index}次循环结束================================================')

            # 循环完1次 累加
            bugcount.append(bug)
            # for end

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 查询成功
        if count > 0:
            code = 200  # 成功
            msg = '查询语句执行成功'

    # except Exception:
    except:
        # 如果发生错误则回滚
        # 输出异常信息
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索开发count方法 type(data)== ', type(data))
    print('<admin.py> 搜索开发方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist> 返回结果==jsonStr=====', json_str)


    print('=================================获取所有项目的数据 end ===================================')
    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str


def testtest():


            #     最终sql
            search_sql = searchsql_not_complete + searchsql_end
            print("《查询项目折线图 - 统计数据 - 拼接的最终sql =============== 》", search_sql)

            # sql参数 + 起始终止时间
            search_sql_args.append(startTime)
            search_sql_args.append(endTime)
            print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

            # 执行sql语句
            cursor.execute(search_sql, search_sql_args)
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果
            sql_return_result_tuple = cursor.fetchall()

            #转换查询结果为[{},{},{}]这种格式的
            print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
            print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
            print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
            print("sql语句执行成功")


            bug = dict()
            # 给需要累加的 赋初始值
            forum_project = 0
            for i in sql_return_result_tuple:
                bug['totalNumByProjectBelongProjectSum' + str(forum_project)] = 0
                bug['addNumByProjectBelongProjectSum' + str(forum_project)] = 0
                bug['closeNumByProjectBelongProjectSum' + str(forum_project)] = 0
                forum_project += 1

            rank = 1

            print('?????????????????? sql_return_result_tuple 时间==', sql_return_result_tuple[0])
            print('?????????????????? sql_return_result_tuple 时间 type ==', type(sql_return_result_tuple[0]))

            forum_project = 0 # 重新赋值0，给下一个循环用
            for r in sql_return_result_tuple:
            # for r in date_tuple:

                bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
                date = str(r[0])
                bug['project'] = r[1]  # 项目名称
                bug['addNumByProject'] = r[2]  # 新增
                bug['closeNumByProject'] = r[3]  # 关闭
                bug['regressionNumByProject'] = r[4]  # 回归
                bug['delayNumByProject'] = r[5]  # 延迟
                bug['addLeve12NumByProject'] = r[6]  # 12级bug新增
                bug['closeLevel12NumByProject'] = r[7]  # 1-2级bug关闭
                bug['regressionLeve12NumByProject'] = r[8]  # 1-2级bug回归
                bug['delayLeve12NumByProject'] = r[9]  # 1-2级bug延迟
                bug['totalLevel12NumByProject'] = r[10]  # 1-2级bug总数
                bug['bugCloseRateByProject'] = float(r[11])  # bug解决率(关闭/总数) 是decimall类型，转成float
                bug['rankByProjectByProject'] = rank  #排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1
                bug['totalNumByProject'] = r[12]  # 总数
                # bug['totalNumByProjectBelongProject0'] = r[13]  # 总数

                bug['totalNumByProjectBelongProject' + str(forum_project)] = r[13 + forum_project]  # 属于项目0的全部bug
                print('????????????????????????????????????r[13 + fornum] =========', r[13 + fornum])
                bug['addNumByProjectBelongProject' + str(forum_project)] = r[13 + forum_project]  # 属于项目0的新增bug
                bug['closeNumByProjectBelongProject' + str(forum_project)] = r[13 + forum_project]  # 属于项目0的关闭bug




                for project_num in date_tuple:
                    bug['totalNumByProjectBelongProjectSum' + str(forum_project)] += r[13 + forum_project * 3]  # 属于项目0的全部bug
                    bug['addNumByProjectBelongProjectSum' + str(forum_project)] += r[13 + forum_project * 3 + 1]  # 属于项目0的新增bug
                    bug['closeNumByProjectBelongProjectSum' + str(forum_project)] += r[13 + forum_project * 3 + 2]  # 属于项目0的关闭bug

                    print(f'????????? 第{forum_project}次循环，日期{date}---- 前后对比 bug总数（前，后），新增总数（前，后）， 关闭总数（前后） =========',
                          r[13 + forum_project * 3], bug['totalNumByProjectBelongProjectSum' + str(forum_project)],
                          r[13 + forum_project * 3 + 1], bug['addNumByProjectBelongProjectSum' + str(forum_project)],
                          r[13 + forum_project * 3 + 2], bug['closeNumByProjectBelongProjectSum' + str(forum_project)]
                          )

                rank += 1
                print('==============循环person==', bug)

                forum_project += 1

                bugcount.append(bug)  # 装的是每天的数量
            # for 循环添加data 完成

            print('????dbutil 转换完的【{}】格式数据users==', bugcount)


            # 拼接返回数据,返回列表
            count = len(sql_return_result_tuple)  # sql语句结果个数

            # 判断是否 能登录
            # if count > 0:
            code = 200  # 成功
            msg = '查询语句执行成功'
