"""
管理buglist：
增删改查


"""

import pymysql
import json
#  引入python中的traceback模块，跟踪错误
import traceback
from py import utils
import datetime
import time

# 数据库配置
db_config_dict = utils.get_dbargs_from_config_byabspath()
# db_config_dict = utils.get_dbargs_from_config()

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

# 获取bug总数
def get_buglist_totalnum():
    #  定义初始数据
    data = {}
    buglist = []
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        sql = 'select count(bugid) from bugcount.buglist'
        print('sql语句为==', sql)

        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()
        print(sql_return_result_tuple)

        # 拼接返回数据,返回列表
        count = sql_return_result_tuple[0]  # sql语句结果个数
        # 顺利执行完毕就算成功
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
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist.py> 查询bug总数返回json_str=', json_str)
    return json_str


# 获取bug总数-返回num
def get_buglist_totalnum_returnnum():
    # 1. 定义初始数据
    bug_totalnum = 0

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        sql = 'select count(bugid) from bugcount.buglist'
        print('sql语句为==', sql)

        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()
        print(sql_return_result_tuple)

        # 拼接返回数据,返回列表
        bug_totalnum = sql_return_result_tuple[0]  # sql语句结果个数- 返回的是一个tuple
        print("============类型", type(bug_totalnum))
        # 顺利执行完毕就算成功
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

    return bug_totalnum


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
        sql = 'select bugid, bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, regression_times, reopen_times, submitterindex from bugcount.buglist limit %s,%s'

        print(f'sql语句为==', sql)
        # print(f'sql语句参数 *args====  page={page},limit={limit}')

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
            # 日期日过查出来是None,前端显示 ''
            if bug['bug_submit_date'] == 'None':
                bug['bug_submit_date'] = ''
            bug['project'] = r[2]
            bug['software'] = r[3]
            bug['test_version'] = r[4]
            bug['bug_description'] = r[5]
            bug['severity_level'] = r[6] # 转成int 否则报错TypeError: not all arguments converted during string formatting
            bug['priority'] = r[7]
            bug['bug_difficulty'] = r[8]
            bug['bug_status'] = r[9]
            # 前端显示为中文字符，1 处理(handle)，2 关闭(close)，3 回归(regression)，4 延迟(delay)， 5 重开(reopen) 0.未知
            if bug['bug_status'] == 1:
                bug['bug_status'] = "处理"
            elif bug['bug_status'] == 2:
                bug['bug_status'] = "关闭"
            elif bug['bug_status'] == 3:
                bug['bug_status'] = "回归"
            elif bug['bug_status'] == 4:
                bug['bug_status'] = "延迟"
            elif bug['bug_status'] == 5:
                bug['bug_status'] = "重开"
            else:
                bug['bug_status'] = "未知"  # 未知（可能用户上传时bug_status字段不对）

            bug['bug_close_date'] = str(r[10])  # 转成str，否则会报TypeError: Object of type datetime is not JSON serializable
            # 日期如果查出来是None,前端显示 ''
            if bug['bug_close_date'] == 'None':
                bug['bug_close_date'] = ''
            bug['close_version'] = r[11]
            bug['cause_analysis'] = r[12]
            bug['bug_img'] = r[13]
            bug['intermediate_situation'] = r[14]
            bug['developer'] = r[15]
            bug['remark'] = r[16]
            bug['regression_times'] = str(r[17])
            if bug['regression_times'] == 'None':
                bug['regression_times'] = ''
            bug['reopen_times'] = r[18]
            if bug['reopen_times'] == 'None':
                bug['reopen_times'] = ''
            bug['submitterindex'] = r[19]
            # print('==============循环person==', bug)

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
        msg = 'ssss'
        traceback.print_exc()
        print('出现异常，sql语句执行失败')
        # print('出现异常，sql语句执行失败', Exception)
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    # 获取数据总数
    count = get_buglist_totalnum_returnnum()[0]
    print("=====================bug总数", count)
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
    print('<buglist.py> (search_buglist)返回jsonStr=====', json_str)
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
def add_bug(*args):  # 建议传的时候就是list
    # 0. 将参数强转成list
    args = list(args)
    print("args==============", args)

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    # 1. 定义json数据
    data = {}
    buglist = []
    code = 500  # 默认失败
    errorcode = 0  # 错误码，主要是pymysql的错误码
    msg = '添加失败'
    count = 0  # sql语句执行结果个数
    is_args_legal = True  # 默认参数合法


    # 2. 判断参数是否合法，主要判断日期格式
    print("==========================传入参数args", args)  # tuple
    if utils.is_valid_date(args[0]) is False or utils.is_valid_date(args[9]) is False:  # 判断日期格式
        msg = '日期格式错误，请检查"提交日期"和"关闭日期"列'
        is_args_legal = False
    if args[4] == 'NaN' or args[4] == '' or args[4] == None:  # 判断描述是否为空
        msg = '描述不能为空，请检查'
        is_args_legal = False
    print("sssss????????????????????????????",args[18])
    if args[18] == 'NaN' or args[18] == '' or args[18] == None:  # 判断submitterindex是否为空
        msg = '提交者索引不能为空，请检查'
        is_args_legal = False

    if is_args_legal is True:
        # 3.打开数据库连接
        conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()

        # 使用 execute()  方法执行 SQL 查询
        try:
            # 默认bugid 是null 就按顺序加入mysql
            sql = 'insert into bugcount.buglist (bug_submit_date, project, software, test_version,' \
                                            ' bug_description, severity_level, priority, bug_difficulty, bug_status,' \
                                            ' bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation,' \
                                            ' developer, remark, regression_times, reopen_times, submitterindex) ' \
                  ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            print(f'sql语句为==', sql)
            # print('sql语句参数 *args==== }', args)
            for i in args:
                index = args.index(i)
                print(f'sql语句参数 *args{index} type==== ', args[index])
                if args[index] == 'NaN' or args[index] == '':
                    args[index] = None

            print('sql语句参数 *args type==== }', type(args))

            # 判断传入的日期参数 ，如果是空的话，不给sql语句传值就可以了，但是args是tuple类型，不支持删除--》转成list，将time替换成None
            args_list = list(args)  # tuple --> list
            if args[1] == '' or args[0] == 'None':  # 开始时间
                print('将time赋值None')
                args_list[1] = '0000-00-00'  # 转成None
                print('args_list[1] = ', args_list[1])
            if args[10] == '' or args[9] == 'None':  # 关闭时间
                print('将time赋值None')
                # args_list[10] = None  # 转成None
                args_list[10] = '0000-00-00'  # 转成None
                print('args_list[1] = ', args_list[10])

            print('sql语句参数 转换后  *args==== }', args)

            # 多参数，execute要传2个参数，sql 和args分解出来的
            print('type(args)===================================', type(args))
            # cursor.execute(sql, args)  # 偶尔不好用
            args_test = [args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10],
                args[11], args[12], args[13], args[14], args[15], args[16], args[17], args[18]]  # 测试用

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

            # 拼接返回数据,返回列表
            count = len(sql_return_result_tuple)  # sql语句结果个数
            # 判断是否 能登录
            code = 200  # 成功
            msg = 'add bug语句执行成功'

        # except Exception:
        except pymysql.Error as e:
            # 输出异常信息，如果发生错误则回滚
            print("==============错误")
            # print(e)  # (1062, "Duplicate entry 'sss' for key 'submitterindex'")
            print(e.args[0], e.args[1])  # args[0]->code  args[1]-->原因
            if e.args[0] == 1062:
                errorcode = 1062  # 索引重复
            # traceback.print_exc()  # 暂时不用，打印内容过多
            print('出现异常，sql语句执行失败')
            # print('出现异常，sql语句执行失败', Exception)
            conn.rollback()
        finally:
            # 不管是否异常，都关闭数据库连接
            cursor.close()
            conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['errorcode'] = errorcode
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist.py> (add_bug) 返回jsonStr=====', json_str)
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
              "count(bug_status = 5 or null) as 'reopen', " \
              "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
              "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
              "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
              "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
              "count(bug_status = 5 and severity_level <= 2 or null) as 'reopen12', " \
              "count(severity_level <= 2 or null) as 'total12', " \
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
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        # print("sql语句执行成功")

        rank = 1
        for r in sql_return_result_tuple:
            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['project'] = r[1]  # 项目名称
            bug['addNumByProject'] = r[2]  # 新增
            bug['closeNumByProject'] = r[3]  # 关闭
            bug['regressionNumByProject'] = r[4]  # 回归
            bug['delayNumByProject'] = r[5]  # 延迟
            bug['reopenNumByProject'] = r[6]  # 重开

            bug['addLeve12NumByProject'] = r[7]  # 12级bug新增
            bug['closeLevel12NumByProject'] = r[8]  # 1-2级bug关闭
            bug['regressionLeve12NumByProject'] = r[9]  # 1-2级bug回归
            bug['delayLeve12NumByProject'] = r[10]  # 1-2级bug延迟
            bug['reoepnLeve12NumByProject'] = r[11]  # 1-2级bug重开
            bug['totalLevel12NumByProject'] = r[12]  # 1-2级bug总数
            bug['bugCloseRateByProject'] = float(r[13])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rankByProjectByProject'] = rank  #排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1
            bug['totalNumByProject'] = r[14]  # 总数
            rank += 1
            # print('==============循环person==', bug)

            bugcount.append(bug)
        # print('????dbutil 转换完的【{}】格式数据users==', bugcount)

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
    # print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    # print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('《buglist.py》 /get_bugcount_by_project  -->jsonStr== ', json_str)
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
            # print(f'当前第{fornum}项 循环：第{fornum}项目为', i, project_tuple[fornum])
            # print('项目有：', project_tuple)
            # print('项目 长度len(project_tuple)====', len(project_tuple))
            # print('拼接sql语句')
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
        # print("《查询项目折线图 - 统计数据 - sql = 》", search_sql)

        # sql参数 + 起始终止时间
        search_sql_args.append(startTime)
        search_sql_args.append(endTime)
        # print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

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

                """
                print(f'????????? 第{forum_project}次循环，日期{date}---- 前后对比 bug总数（前，后），新增总数（前，后）， 关闭总数（前后） =========',
                      r[13 + forum_project * 3], bug['totalNumByProjectBelongProjectSum' + str(forum_project)],
                      r[13 + forum_project * 3 + 1], bug['addNumByProjectBelongProjectSum' + str(forum_project)],
                      r[13 + forum_project * 3 + 2], bug['closeNumByProjectBelongProjectSum' + str(forum_project)]
                      )
                """

            rank += 1
            # print('==============循环person==', bug)

            forum_project += 1

            bugcount.append(bug)  # 装的是每天的数量
        # for 循环添加data 完成

        # print('????dbutil 转换完的【{}】格式数据users==', bugcount)


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
    # print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    # print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('《buglist》 get_bugcount_by_project_orderby_time_error_nouse ==> jsonStr==', json_str)

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
            # print(f'当前第{fornum}项 循环：第{fornum}项目为', i, project_tuple[fornum])
            # print('项目有：', project_tuple)
            # print('项目 长度len(project_tuple)====', len(project_tuple))
            # print('拼接sql语句')
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
            # print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

        #     最终sql
        search_sql = searchsql_not_complete + searchsql_end
        # print("《查询项目折线图 - 统计数据 - sql = 》", search_sql)

        # sql参数 + 起始终止时间
        search_sql_args.append(startTime)
        search_sql_args.append(endTime)
        # print('for 循环中 拼接成的sq 参数 search_sql_args==', search_sql_args)

        # 执行sql语句
        cursor.execute(search_sql, search_sql_args)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        #转换查询结果为[{},{},{}]这种格式的
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        # print("sql语句执行成功")

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
            # print('==============循环person==', bug)

            bugcount.append(bug)  # 装的是每天的数量
        # for 循环添加data 完成

        print('<buglist.py> get_bugcount_by_project_orderby_time 转换完的【{}】格式数据bugcount==', bugcount)


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
    # print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    # print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist.py> get_bugcount_by_project_orderby_time  ==>jsonStr=====', json_str)

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

        print(f'<bulist.py> get_bugcount_by_developer,sql语句为==', sql)
        print('<bulist.py>  get_bugcount_by_developer,sql, 语句参数starTime,end Time =={args}', startTime, endTime)

        # 执行sql语句

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        cursor.execute(sql, [startTime, endTime])
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        #转换查询结果为[{},{},{}]这种格式的
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        # print("sql语句执行成功")

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
            # print('==============循环person==', bug)

            bugcount.append(bug)
        print('<bulist.py>  get_bugcount_by_developer,sql  转换完的【{}】格式数据 bugcount==', bugcount)

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
    # print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    # print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<bulist.py>  get_bugcount_by_developer,sql ==>jsonStr=====', json_str)
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
    print(f'app.py 传的参数startime={startTime}，endtime= {endTime}')

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    bugcount = []
    #默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数

        # 1. 获取有几个project
        get_project_sql = 'select project from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and project is not null group by project'
        cursor.execute(get_project_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        project_tuple = cursor.fetchall()


        print(f'1. 获取有多少项目==={project_tuple}')
        """
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
        """
        # ppname = str1808[1:len(str1808)-2]
        # print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取（"1808",） 1-len(str)-2', ppname)

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
                                  "count(bug_status = 5 or null) as 'reopen', " \
                                  "count(bug_status = 1 and severity_level <= 2 or null) as 'add12', " \
                                  "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                  "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                  "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                  "count(bug_status = 5 and severity_level <= 2 or null) as 'reopen12', " \
                                  "count(severity_level <= 2 or null) as 'delay12', " \
                                  "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                  "count(bugid or null) as 'totalNum' "

        searchsql_end =  " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by bug_submit_date order by bug_submit_date"
        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        search_sql_args = list()
        # print('未拼接好的字符串==', searchsql_not_complete + searchsql_end)

        search_sql_middle_about_project = ""
        # 循环拼接字符串
        for project in project_tuple:
            # 当前索引
            print(f'当前project=={str(project)}')
            index = project_tuple.index(project)
            project_name_tuple_to_str = str(project_tuple[index])
            project_name = project_name_tuple_to_str[1:len(project_name_tuple_to_str)-2]
            # print('循环中的项目名str==', project_name)


            # print(f'当前第{index}项 循环：第{index}项目为', project_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为项目1 / 属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug

            # project='1808' as project0
            sql_name_project = ",project=" + project_name + "as project" + str(index)
            # print('name ==========', sql_name_project)

            sql_add_num_byproject_belong_project = ",count(bug_status=1 and project = " + project_name + "or null) as add_num_project" + str(index)
            sql_close_num_byproject_belong_project = ",count(bug_status=2 and project = " + project_name + "or null) as close_num_project" + str(index)
            sql_regression_num_byproject_belong_project = ",count(bug_status=3 and project = " + project_name + "or null) as regression_num_project" + str(index)
            sql_delay_num_byproject_belong_project = ",count(bug_status=4 and project = " + project_name + "or null) as delay_num_project" + str(index)
            sql_reopen_num_byproject_belong_project = ",count(bug_status=5 and project = " + project_name + "or null) as delay_num_project" + str(index)
            """
            print('for 循环拼接的sql == ', sql_name_project + sql_add_num_byproject_belong_project +sql_close_num_byproject_belong_project +
                  sql_regression_num_byproject_belong_project + sql_delay_num_byproject_belong_project)
            """
            for_sql = sql_name_project + sql_add_num_byproject_belong_project +sql_close_num_byproject_belong_project + sql_regression_num_byproject_belong_project + sql_delay_num_byproject_belong_project +sql_reopen_num_byproject_belong_project
            # search_sql_middle_about_project 基础上拼接
            search_sql_middle_about_project += for_sql
            # print('项目相关sql 拼接结果==', search_sql_middle_about_project)


        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_project + searchsql_end
        print('<bulist.py> get_allprojectdata_withproject_orderby_date, 最终sql ==', search_sql)

        # 2. 执行sql语句
        cursor.execute(search_sql, [startTime, endTime])
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        # print("sql语句执行成功")

        rank = 1 # 排名
        # 3. 整理返回给前端的值,相当于按时间循环
            # 返回数据 第几行 第几列xx数据
        for r in sql_return_result_tuple:
            # print('=======================r=', r)

            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            # print('========================bug_submit_date', bug['bug_submit_date'])
            bug['project'] = r[1]  # 项目名称
            bug['add'] = r[2]  # 新增
            bug['close'] = r[3]  # 关闭
            bug['regression'] = r[4]  # 回归
            bug['delay'] = r[5]  # 延迟
            bug['reopen'] = r[6]  # 重开

            bug['add12'] = r[7]  # 12级bug新增
            bug['close12'] = r[8]  # 1-2级bug关闭
            bug['regression12'] = r[9]  # 1-2级bug回归
            bug['delay12'] = r[10]  # 1-2级bug延迟
            bug['reopen12'] = r[11]  # 1-2级bug重开

            bug['total12'] = r[12]  # 1-2级bug总数
            bug['bugCloseRate'] = float(r[13])  # bug解决率(关闭/总数) 是decimall类型，转成float
            bug['rank'] = rank  # 排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1，不是从数据库查的，自己算的
            bug['totalNum'] = r[14]  # 总数

            # 后面是项目相关的 关闭情况，有几个项目循环几次
            for project in project_tuple:
                # 当前索引
                # print(f'当前project=={str(project)}')
                index = project_tuple.index(project)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                # project0

                #   str1808[1:len(str1808)-2] 截取字符串 中project名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中project名字--》1808 (去掉''格式的)
                bug['project' + str(index)] = str(project)[2:len(str(project))-3]  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出
                bug['add_project' + str(index)] = r[15 + 6*index + 1]
                bug['close_project' + str(index)] = r[15 + 6*index + 2]
                bug['regression_project' + str(index)] = r[15 + 6*index + 3]
                bug['delay_project' + str(index)] = r[15 + 6*index + 4]
                bug['reopen_project' + str(index)] = r[15 + 6*index + 5]

                # print(f'project{index}=', bug['project' + str(index)])  #
                # print(f'add_project{index}=', bug['add_project' + str(index)])
                # print(f'close_project{index} ==', bug['close_project' + str(index)])
                # print(f'regression_project{index}  ===', bug['regression_project' + str(index)])
                # print(f'delay_project{index}  ===', bug['delay_project' + str(index)])
                #
                # print(f'第{index}次循环结束================================================')

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
    # print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    # print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<bulist.py> 获取每日数据get_allprojectdata_withproject_orderby_date, 返回结果==jsonStr=====', json_str)
    print('=================================获取所有项目的数据 end ===================================')
    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str


# 获取所有项目的 每日累加数据，为了画折线图project0 - project13(默认给13个项目，没有值默认不返回数据, ！！ 有几个项目返回几个项目的值)
def get_allprojectdata_everyday_sum_withproject_orderby_date(startTime, endTime):
    print('=================================获取所有项目 每日累加的数据 start ===================================')
    print(f'《app.py》get_allprojectdata_everyday_sum_withproject_orderby_date， 传的参数{startTime}， {endTime}')

    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    #0. 先获取有多少个项目///////////////////////////////////////////////
    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个project
        get_project_sql = 'select project from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and project is not null group by project'
        cursor.execute(get_project_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        project_tuple = cursor.fetchall()

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

    #1. 先获取每日的数据/////////////////////////////////////////
    json_str_everyday = get_allprojectdata_withproject_orderby_date(startTime, endTime)

    # 2. 解析data ,进行累加
    # print('每日数据==', json_str_everyday)
    # 先json.loads 转成dict形式
    json_dict = json.loads(json_str_everyday)
    # print('code==', json_dict['code'])
    # print('msg==', json_dict['msg'])
    # print('count==', json_dict['count'])
    # print('data==', json_dict['data'])
    # print('data.len==', len(json_dict['data']))
    # print('data.type==', type(json_dict['data']))  # list
    #
    # print('data.list[0]==', json_dict['data'][0])  # list
    # print('data.list[0] type==', type(json_dict['data'][0]))  # dict


    # 定义基础数据
        # bug_submit_date', title: '时间', sort: true, width: 120}
        #   'project', title: '项目'
    addsum = 0
    closesum = 0
    regressionsum = 0
    delaysum = 0
    add12sum = 0
    close12sum = 0
    regression12sum = 0
    delay12sum =0
    total12sum = 0
    bugCloseRatesum = 0
    ranksum = 0
    totalNumsum = 0

    # 项目相关变量 先定义13个项目变量用到了就用- 使用字典
    project_key_value_dict = dict()
    for project in project_tuple:
        project_index = project_tuple.index(project)
        # addsum_project0 = 0
        project_key_value_dict['addsum_project' + str(project_index)] = 0
        project_key_value_dict['closesum_project' + str(project_index)] = 0
        project_key_value_dict['regressionsum_project' + str(project_index)] = 0
        project_key_value_dict['delaysum_project' + str(project_index)] = 0



    # 除了时间外全部累加
    datas_everyday_list = json_dict['data']
    for r in datas_everyday_list:
        index = datas_everyday_list.index(r)
        date = datas_everyday_list[index]['bug_submit_date']
        # print(f'当前 第{index}次时间循环，日期{date}')

        bug = dict()
        # print('addsum=', addsum)
        # print('bug[add]', bug['add'])

        addsum += r['add']
        closesum += r['close']
        regressionsum += r['regression']
        delaysum += r['delay']
        add12sum += r['add12']
        close12sum += r['close12']
        regression12sum += r['regression12']
        delay12sum += r['delay12']
        total12sum += r['total12']
        bugCloseRatesum += r['bugCloseRate']
        ranksum += r['rank']
        totalNumsum += r['totalNum']


        bug['bug_submit_date'] = str(r['bug_submit_date'])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
        bug['project'] = r['project']  # 项目名称
        bug['add'] = addsum  # 新增
        bug['close'] = closesum  # 关闭
        bug['regression'] = regressionsum  # 回归
        bug['delay'] = delaysum  # 延迟
        bug['add12'] = add12sum  # 12级bug新增
        bug['close12'] = close12sum  # 1-2级bug关闭
        bug['regression12'] = regression12sum  # 1-2级bug回归
        bug['delay12'] = delay12sum # 1-2级bug延迟
        bug['total12'] = total12sum # 1-2级bug总数
        bug['bugCloseRate'] = float(bugCloseRatesum)  # bug解决率(关闭/总数) 是decimall类型，转成float
        bug['rank'] = ranksum  # 排名 sql未查出来，自己算,因为sql查出来是根据 解决率 倒序的，第一个是排名第1，不是从数据库查的，自己算的
        bug['totalNum'] = totalNumsum  # 总数

        for project in project_tuple:
            project_index = project_tuple.index(project)

            # 累加数据--》 赋值给addsum 这种变量         # 项目0-13相关 - 累加
            project_key_value_dict['addsum_project' + str(project_index)] += r['add_project' + str(project_index)]
            project_key_value_dict['closesum_project' + str(project_index)] += r['close_project' + str(project_index)]
            project_key_value_dict['regressionsum_project' + str(project_index)] += r['regression_project' + str(project_index)]
            project_key_value_dict['delaysum_project' + str(project_index)] += r['delay_project' + str(project_index)]

            bug['project' + str(project_index)] = r['project0']  # 项目0名称
            bug['add_project' + str(project_index)] = project_key_value_dict['addsum_project' + str(project_index)]  # 项目0新增
            bug['close_project' + str(project_index)] = project_key_value_dict['closesum_project' + str(project_index)]  # 项目0关闭
            bug['regression_project' + str(project_index)] = project_key_value_dict['regressionsum_project' + str(project_index)]  # 项目0回归
            bug['delay_project' + str(project_index)] = project_key_value_dict['delaysum_project' + str(project_index)]  # 项目0延迟

        # print('bug==', bug)
        bugcount.append(bug)

    #     按顺序执行完，就认为成功了
    code = 200
    msg = 'sql语句执行成功'
    count = len(bugcount)


    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('《app.py》get_allprojectdata_everyday_sum_withproject_orderby_date，返回结果==jsonStr=====', json_str)

    print('=================================获取所有项目 每日累加数据 end ===================================')
    return json_str


# 获取所有项目的 获取新增bug(status=1) 今天相对昨天的增长和关闭情况，为了画折线图project0 - project13(默认给13个项目，没有值默认不返回数据, ！！ 有几个项目返回几个项目的值)
def get_allprojectdata_withproject_alongtime_newbug_addandclose_orderby_date(startTime, endTime, timeDifference):
    print('=================================获取新增bug(status=1) 今天相对昨天的增长和关闭情 start ===================================')
    print(f'<app.py> get_allprojectdata_withproject_everyday_newbug_addandclose_orderby_date, 传的参数{startTime}， {endTime}, {timeDifference}，类型{type(startTime)}， {type(endTime)}, {type(timeDifference)}')

    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    #0. 先获取有多少个项目///////////////////////////////////////////////
    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个project
        get_project_sql = 'select project from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and project is not null group by project'
        cursor.execute(get_project_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        project_tuple = cursor.fetchall()

        # 2.获取有多少时间点 list
        bug_submit_date_list = utils.get_bug_submit_date_list_return_countsqltime(startTime, endTime, timeDifference)
        bug_submit_date_list_rel = utils.get_bug_submit_date_list(startTime, endTime, timeDifference)
        print('获取时间列表 bug_submit_date_list', bug_submit_date_list)
        print('获取时间列表 bug_submit_date_list_rel', bug_submit_date_list)
        # print('获取时间列表。type bug_submit_date_list.type = ', type(bug_submit_date_list))

        # 3.循环执行sql语句,获取bug_submit_date_list 中时间节点的数据

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project,count(bug_status = 1 or null) as 'add', " \
                                 "count(bug_status = 2 or null) as 'close'"
        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date < %s )"

        search_sql_middle_about_project = ""
        # 循环拼接字符串
        for project in project_tuple:
            # 当前索引
            print(f'当前project=={str(project)}')
            index = project_tuple.index(project)
            project_name_tuple_to_str = str(project_tuple[index])
            project_name = project_name_tuple_to_str[1:len(project_name_tuple_to_str) - 2]
            # print('循环中的项目名str==', project_name)

            # print(f'当前第{index}项 循环：第{index}项目为', project_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为项目1 / 属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug

            # project='1808' as project0
            sql_name_project = ",project=" + project_name + " as project" + str(index)
            # print('name ==========', sql_name_project)
            sql_add_num_byproject_belong_project = " ,count(bug_status=1 and project =" + project_name + " or null) as add_num_project" + str(index)
            sql_close_num_byproject_belong_project = ", count(bug_status=2 and project =" + project_name + " or null) as close_num_project" + str(index)

            # print('for 循环拼接的sql == ', sql_name_project + sql_add_num_byproject_belong_project + sql_close_num_byproject_belong_project)

            for_sql = sql_name_project + sql_add_num_byproject_belong_project + sql_close_num_byproject_belong_project
            # search_sql_middle_about_project 基础上拼接
            search_sql_middle_about_project += for_sql
            # print('项目相关sql 拼接结果==', search_sql_middle_about_project)

        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_project + searchsql_end
        print(f'buglist.py.绘制新增bug趋势,最终查询sql ==={search_sql}')  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出

        #  for 执行sql语句,查出结果，循环len(bug_submit_date_list) -1 次,从list取出来直接str设备
        for i in bug_submit_date_list:
            index = bug_submit_date_list.index(i)
            if index == len(bug_submit_date_list) - 1:
                break

            # print(f'绘制新增bug增长曲线和关闭曲线，当前循环{index}, 值{i}, 值类型{type(i)}, str值{str(i)} ')
            starttime_forsql = bug_submit_date_list[index]
            endtime_forsql = bug_submit_date_list[index + 1]
            endtime = bug_submit_date_list_rel[index + 1]  # 真实的结束时间
            # print(f'起始时间{startTime}， 终止时间{endTime}，时间type{type(endTime)}')

            cursor.execute(search_sql, [starttime_forsql, endtime_forsql])
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果, 包括：时间,项目，新增，关闭，项目0，项目0新增，项目0关闭，项目1。。。。
            sql_return_result_tuple = cursor.fetchall()
            print(f'buglist.py.绘制新增bug趋势，返回结果=={sql_return_result_tuple}')

            # 3. 解析结果，加入到bugcount list表中，每次只返回一条数据所以不用for循环了

            bug = dict()
            print(f'buglist.py.绘制新增bug趋势,tuple[0]', sql_return_result_tuple[0])
            print(f'buglist.py.绘制新增bug趋势,tuple[0][0]', sql_return_result_tuple[0][0])
            print(f'buglist.py.绘制新增bug趋势,tuple[0][1]', sql_return_result_tuple[0][1])

            bug['bug_submit_date'] = str(endtime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['project'] = sql_return_result_tuple[0][1]  # 项目名称
            bug['add'] = sql_return_result_tuple[0][2]  # 新增
            bug['close'] = sql_return_result_tuple[0][3]  # 关闭

            # 后面是项目相关的 关闭情况，有几个项目循环几次
            for project in project_tuple:

                # 当前索引
                print(f'当前 project r=={str(project)}')
                index = project_tuple.index(project)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中 project 名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中 project 名字--》1808 (去掉''格式的)
                bug['project' + str(index)] = str(project)[2:len(str(project))-3]  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出
                bug['add_project' + str(index)] = sql_return_result_tuple[0][4 + 3*index + 1]
                bug['close_project' + str(index)] = sql_return_result_tuple[0][4 + 3*index + 2]

                # print(f'project{index}=', bug['project' + str(index)])  #
                # print(f'add_projectr{index}=', bug['add_project' + str(index)])
                # print(f'close_projectr{index} ==', bug['close_project' + str(index)])

                # print(f'第{index}次循环结束================================================')

            print(f'buglist.py.绘制新增bug趋势,bug===={bug}')
            bugcount.append(bug)
            # for end

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


    #     按顺序执行完，就认为成功了
    code = 200
    msg = 'sql语句执行成功'
    count = len(bugcount)


    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist> ,get_allprojectdata_withproject_everyday_newbug_addandclose_orderby_date,获取新增bug(status=1) 今天相对昨天的增长和关闭情返回结果==jsonStr=====', json_str)

    print('=================================获取新增bug(status=1) 今天相对昨天的增长和关闭情 end ===================================')
    return json_str


# 获取所有项目的 获取all bug(status=1) 一段时间内的增长和关闭情况，为了画折线图project0 - project13(默认给13个项目，没有值默认不返回数据, ！！ 有几个项目返回几个项目的值)
def get_allprojectdata_withproject_alongtime_allbug_orderby_date(startTime, endTime, timeDifference):
    print('=================================获取累计bug趋势（一段时间 - 每个月/周） start ===================================')
    print('只需要返回新增/关闭/剩余 项目0新增/项目0关闭/项目0剩余 ')
    print(f'<buglist.py> 累计bug趋势, 传的参数{startTime}， {endTime}, {timeDifference}，类型{type(startTime)}， {type(endTime)}, {type(timeDifference)}')

    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    #0. 先获取有多少个项目///////////////////////////////////////////////
    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个project
        get_project_sql = 'select project from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and project is not null group by project'
        cursor.execute(get_project_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        project_tuple = cursor.fetchall()

        # 2.获取有多少时间点 list
        bug_submit_date_list = utils.get_bug_submit_date_list(startTime, endTime, timeDifference)
        print('获取时间列表 bug_submit_date_list', bug_submit_date_list)
        # print('获取时间列表。type bug_submit_date_list.type = ', type(bug_submit_date_list))

        # 3.循环执行sql语句,获取bug_submit_date_list 中时间节点的数据

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project," \
                                 "count(bug_status=1 or null) as 'add', " \
                                 "count(bug_status = 2 or null) as 'close'," \
                                 "count(bug_status = 3 or null) as 'regression', " \
                                 "count(bug_status = 4 or null) as 'delay', " \
                                 "count(bug_status = 5 or null) as 'reopen', " \
                                 "count(severity_level <= 2 or null) as 'add12', " \
                                 "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                 "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                 "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                 "count(bug_status = 5 and severity_level <= 2 or null) as 'reopen12', " \
                                 "count(severity_level <= 2 or null) as 'total12', " \
                                 "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                 "count(bugid or null) as 'totalNum' "

        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )"

        search_sql_middle_about_project = ""
        # 循环拼接字符串
        for project in project_tuple:
            # 当前索引
            print(f'当前project=={str(project)}')
            index = project_tuple.index(project)
            project_name_tuple_to_str = str(project_tuple[index])
            project_name = project_name_tuple_to_str[1:len(project_name_tuple_to_str) - 2]
            # print('循环中的项目名str==', project_name)

            # print(f'当前第{index}项 循环：第{index}项目为', project_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为项目1 / 属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug

            # project='1808' as project0
            sql_name_project = ",project=" + project_name + " as project" + str(index)  # 项目名
            sql_add_num_byproject_belong_project = ",count(bug_status=1 and project = " + project_name + " or null) as add_num_project" + str(index)
            sql_close_num_byproject_belong_project = ",count(bug_status=2 and project = " + project_name + " or null) as close_num_project" + str(index)
            sql_regression_num_byproject_belong_project = ",count(bug_status=3 and project = " + project_name + " or null) as regression_num_project" + str(index)
            sql_delay_num_byproject_belong_project = ",count(bug_status=4 and project = " + project_name + " or null) as delay_num_project" + str(index)
            sql_reopen_num_byproject_belong_project = ",count(bug_status=5 and project = " + project_name + " or null) as reopen_num_project" + str(index)
            sql_total_num_byproject_belong_project = ",count(project = " + project_name + " or null) as total_num_project" + str(index)

            for_sql = sql_name_project + sql_add_num_byproject_belong_project + sql_close_num_byproject_belong_project + sql_regression_num_byproject_belong_project + sql_delay_num_byproject_belong_project + sql_reopen_num_byproject_belong_project + sql_total_num_byproject_belong_project
            # search_sql_middle_about_project 基础上拼接
            search_sql_middle_about_project += for_sql
            # print('项目相关sql 拼接结果==', search_sql_middle_about_project)

        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_project + searchsql_end
        print(f'绘制bug累计趋势，最终查询sql ==={search_sql}')  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出

        #  for 执行sql语句,查出结果，循环len(bug_submit_date_list) -1 次,从list取出来直接str设备
        startTime = bug_submit_date_list[0]
        for i in bug_submit_date_list:
            index = bug_submit_date_list.index(i)
            if index == len(bug_submit_date_list) - 1:
                break

            # print(f'绘制新增bug增长曲线和关闭曲线，当前循环{index}, 值{i}, 值类型{type(i)}, str值{str(i)} ')

            endTime = bug_submit_date_list[index + 1]
            # print(f'起始时间{startTime}， 终止时间{endTime}，时间type{type(endTime)}')

            # 新增数 ，其实是查的一段时间内，提交过的bug数量，不是bugstatus=1 的数量
            # 第一个[startTime, endTime] 给add 用，第2个[startTime, endTime] 给add12 用，第N个[startTime, endTime] 给where参数 用，
            sqlargs = [startTime, endTime]  # list，有几个developer 填几套startTime, endTime

            cursor.execute(search_sql, sqlargs)
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果, 包括：时间,项目，新增，关闭，项目0，项目0新增，项目0关闭，项目1。。。。
            sql_return_result_tuple = cursor.fetchall()
            print(f'绘制bug累计趋势，返回结果=={sql_return_result_tuple}')

            # 3. 解析结果，加入到bugcount list表中，每次只返回一条数据所以不用for循环了
            bug = dict()  # 每一个bug的累计数
            print(f'绘制bug累计趋势,tuple[0]', sql_return_result_tuple[0])
            print(f'绘制bug累计趋势,tuple[0][0]', sql_return_result_tuple[0][0])
            print(f'绘制bug累计趋势,tuple[0][1]', sql_return_result_tuple[0][1])
            print("==============================bug", bug)
            print(bug)
            bug['bug_submit_date'] = str(endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['project'] = sql_return_result_tuple[0][1]  # 项目名称
            bug['add'] = sql_return_result_tuple[0][2]  # 新增
            print('=======================add', bug['add'])
            bug['close'] = sql_return_result_tuple[0][3]  # 关闭
            bug['regression'] = sql_return_result_tuple[0][4]  # 回归
            bug['delay'] = sql_return_result_tuple[0][5]  # 延迟
            bug['reopen'] = sql_return_result_tuple[0][6]  # 重开

            bug['add12'] = sql_return_result_tuple[0][7]  # 新增(1-2级)
            bug['close12'] = sql_return_result_tuple[0][8]  # 关闭(1-2级)
            bug['regression12'] = sql_return_result_tuple[0][9]  # 回归(1-2级)
            bug['delay12'] = sql_return_result_tuple[0][10]  # 延迟(1-2级)
            bug['reopen12'] = sql_return_result_tuple[0][11]  # 重开(1-2级)
            bug['total12'] = sql_return_result_tuple[0][12]  # 总数(1-2级)

            # bug解决率有可能出现none的情况
            if sql_return_result_tuple[0][13] is None:
                bug['bug_close_rate'] = float(0)
            else:
                bug['bug_close_rate'] = float(sql_return_result_tuple[0][13])  # bug解决率

            # bug['rank'] = sql_return_result_tuple[0][12]  # 排名不是从数据库读出来的，而是自己算出来的
            bug['totalNum'] = sql_return_result_tuple[0][14]  # 总数
            print("总数=======",  bug['totalNum'])
            bug['last'] = int(bug['totalNum']) - int(bug['close'])   # 剩余情况自己算的
            # 与2054行重复
            # print('项目名称====', sql_return_result_tuple[0][15])
            # bug['add_project' + str(index)] = sql_return_result_tuple[0][15+index*7]  #
            # bug['close_project' + str(index)] = sql_return_result_tuple[0][16+index*7]
            # bug['regression_project' + str(index)] = sql_return_result_tuple[0][17+index*7]
            # bug['delay_project' + str(index)] = sql_return_result_tuple[0][18+index*7]
            # bug['reopen_project' + str(index)] = sql_return_result_tuple[0][19+index*7]
            # bug['total_project' + str(index)] = sql_return_result_tuple[0][20+index*7]
            # bug['last_project' + str(index)] = sql_return_result_tuple[0][21+index*7]

            # 后面是项目相关的 关闭情况，有几个项目循环几次
            for project in project_tuple:

                # 当前索引
                print(f'当前 project r=={str(project)}')
                projectindex = project_tuple.index(project)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中 project 名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中 project 名字--》1808 (去掉''格式的)
                bug['project' + str(projectindex)] = str(project)[2:len(str(project))-3]  # 【15】第15位是项目名称，项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出
                bug['add_project' + str(projectindex)] = sql_return_result_tuple[0][16 + 7*projectindex]
                bug['close_project' + str(projectindex)] = sql_return_result_tuple[0][17 + 7*projectindex]
                bug['regression_project' + str(projectindex)] = sql_return_result_tuple[0][18 + 7*projectindex]
                bug['delay_project' + str(projectindex)] = sql_return_result_tuple[0][19 + 7*projectindex]
                bug['reopen_project' + str(projectindex)] = sql_return_result_tuple[0][20 + 7*projectindex]
                bug['total_project' + str(projectindex)] = sql_return_result_tuple[0][21 + 7*projectindex]
                bug['last_project' + str(projectindex)] = int(bug['total_project' + str(projectindex)]) - int(bug['close_project' + str(projectindex)])

                # print(f'project{index}=', bug['project' + str(index)])  #
                # print(f'add_projectr{index}=', bug['add_project' + str(index)])
                # print(f'close_projectr{index} ==', bug['close_project' + str(index)])

                # print(f'第{index}次循环结束================================================')

            print(f'绘制新增bug增长曲线和关闭曲线,bug===={bug}')
            bugcount.append(bug)
            # bugcount.append(totalbugtest)
            # for end

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


    #     按顺序执行完，就认为成功了
    code = 200
    msg = 'sql语句执行成功'
    count = len(project_tuple)


    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist> ,累计bug趋势==jsonStr=====', json_str)
    print('=================================获取bug累计趋势 end ===================================')
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
    msg = 'sql语句执行失败，此时间范围内无数据'
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

        """
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
        """
        # ppname = str1808[1:len(str1808)-2]
        # print(f'1. project_tuplen===> tuple[0] type str1808 --> 截取（"1808",） 1-len(str)-2', ppname)

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
        # print('未拼接好的字符串==', searchsql_not_complete + searchsql_end)

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            # print(f'当前 developer =={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str)-2]
            # print('循环中的 developer 名str==', developer_name)


            # print(f'当前第{index}项 循环：第{index}项目为', developer_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为开发1 / 属于开发1的全部bug / 属于开发1的新增bug / 属于开发1的关闭bug

            # project='1808' as project0
            sql_name_developer = ",developer=" + developer_name + " as developer" + str(index)
            # print('name ==========', sql_name_developer)
            # 执行到这没问题

            sql_add_num_bydeveloper_belong_developer = ",count(bug_status=1 and developer = " + developer_name + " or null) as add_num_developer" + str(index)
            sql_close_num_bydeveloper_belong_developer = ",count(bug_status=2 and developer = " + developer_name + " or null) as close_num_developer" + str(index)
            sql_regression_num_bydeveloper_belong_developer = ",count(bug_status=3 and developer = " + developer_name + " or null) as regression_num_developer" + str(index)
            sql_delay_num_bydeveloper_belong_developer = ",count(bug_status=4 and developer = " + developer_name + " or null) as delay_num_developer" + str(index)
            # print('for 循环拼接的sql == ', sql_name_developer + sql_add_num_bydeveloper_belong_developer +sql_close_num_bydeveloper_belong_developer +
            #       sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer)

            for_sql = sql_name_developer + sql_add_num_bydeveloper_belong_developer +sql_close_num_bydeveloper_belong_developer + sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer
            print('for sql ======', for_sql)
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            # print('开发相关sql 拼接结果==', search_sql_middle_about_developer)


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
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        # print("sql语句执行成功")

        rank = 1 # 排名
        # 3. 整理返回给前端的值,相当于按时间循环
            # 返回数据 第几行 第几列xx数据
        for r in sql_return_result_tuple:
            # print('=======================r=', r)

            bug = dict()
            bug['bug_submit_date'] = str(r[0])  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            # print('========================bug_submit_date', bug['bug_submit_date'])
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
                # print(f'当前developer=={str(developer)}')
                index = developer_tuple.index(developer)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                # project0

                #   str1808[1:len(str1808)-2] 截取字符串 中developer名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中developer名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer))-3]  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出
                bug['add_developer' + str(index)] = r[13 + 5*index + 1]
                bug['close_developer' + str(index)] = r[13 + 5*index + 2]
                bug['regression_developer' + str(index)] = r[13 + 5*index + 3]
                bug['delay_developer' + str(index)] = r[13 + 5*index + 4]

                # print(f'developer{index}=', bug['developer' + str(index)])  #
                # print(f'add_developer{index}=', bug['add_developer' + str(index)])
                # print(f'close_developer{index} ==', bug['close_developer' + str(index)])
                # print(f'regression_developer{index}  ===', bug['regression_developer' + str(index)])
                # print(f'delay_developer{index}  ===', bug['delay_developer' + str(index)])
                #
                # print(f'第{index}次循环结束================================================')

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
    print('<buglist> get_allprojectdata_withdeveoper_orderby_date,返回结果==jsonStr=====', json_str)


    print('=================================获取所有项目的数据 end ===================================')
    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str

# ####################### 开发维度 start####################################
# 获取开发维度 所有bug /1-2级别bug 情况
def get_table_withdeveloper_orderby_date(startTime, endTime, timeDifference):
    print('=================================获取开发维度 所有bug /1-2级别bug 情况 start ===================================')
    print(f'<app.py> get_table_withdeveloper_orderby_date, 传的参数{startTime}， {endTime}, {timeDifference}，类型{type(startTime)}， {type(endTime)}, {type(timeDifference)}')

    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    #0. 先获取有多少个项目///////////////////////////////////////////////
    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个project
        get_developer_sql = 'select developer from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and developer != "" group by developer'
        cursor.execute(get_developer_sql, [startTime, endTime])
        conn.commit()
        #     获取project tuple
        developer_tuple = cursor.fetchall()
        print('<buglist.py> ,开发维度每日数据', developer_tuple)
        print(developer_tuple)

        # 2.获取有多少时间点 list
        bug_submit_date_list = utils.get_bug_submit_date_list(startTime, endTime, timeDifference)
        print('获取时间列表 bug_submit_date_list', bug_submit_date_list)
        # print('获取时间列表。type bug_submit_date_list.type = ', type(bug_submit_date_list))

        # 3.循环执行sql语句,获取bug_submit_date_list 中时间节点的数据

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project," \
                                 "count((bug_submit_date>=%s and bug_submit_date <=%s) or null) as 'add', " \
                                 "count(bug_status = 2 or null) as 'close'," \
                                 "count(bug_status = 3 or null) as 'regression', " \
                                 "count(bug_status = 4 or null) as 'delay', " \
                                 "count((bug_submit_date>=%s and bug_submit_date <=%s) and severity_level <= 2 or null) as 'add12', " \
                                 "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                 "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                 "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                 "count(severity_level <= 2 or null) as 'total12', " \
                                 "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                 "count(bugid or null) as 'totalNum' "

        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )"

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            # print(f'当前 developer=={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str) - 2]
            # print('循环中的 开发 名str==', developer_name)

            # print(f'当前第{index}项 循环：第{index}项目为', developer_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为项目1 / 属于项目1的全部bug / 属于项目1的新增bug / 属于项目1的关闭bug

            # developer='1808' as developer0
            sql_name_developer = ",developer=" + developer_name + "as developer" + str(index)
            # print('name ==========', sql_name_developer)

            sql_add_num_bydeveloper_belong_developer = ",count((bug_submit_date>=%s and bug_submit_date <=%s) and developer = " + developer_name + "or null) as add_num_developer" + str(index)
            sql_close_num_bydeveloper_belong_developer = ",count(bug_status=2 and developer = " + developer_name + "or null) as close_num_developer" + str(index)
            sql_regression_num_bydeveloper_belong_developer = ",count(bug_status=3 and developer = " + developer_name + "or null) as regression_num_developer" + str(index)
            sql_delay_num_bydeveloper_belong_developer = ",count(bug_status=4 and developer = " + developer_name + "or null) as delay_num_developer" + str(index)
            sql_total_num_bydeveloper_belong_developer = ",count(developer = " + developer_name + "or null) as total_num_developer" + str(index)
            """
            print('for 循环拼接的sql == ', sql_name_developer + sql_add_num_bydeveloper_belong_developer +sql_close_num_bydeveloper_belong_developer +
                  sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer + sql_total_num_bydeveloper_belong_developer)
            """
            for_sql = sql_name_developer + sql_add_num_bydeveloper_belong_developer + sql_close_num_bydeveloper_belong_developer + sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer + sql_total_num_bydeveloper_belong_developer
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            # print('项目相关sql 拼接结果==', search_sql_middle_about_developer)

        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_developer + searchsql_end
        print(f'最终查询sql ==={search_sql}')  # 项目名称并不是从sql语句中读出来的，而是单独查询 developer sql语句中读出

        #  for 执行sql语句,查出结果，循环len(bug_submit_date_list) -1 次,从list取出来直接str设备
        for i in bug_submit_date_list:
            index = bug_submit_date_list.index(i)
            if index == len(bug_submit_date_list) - 1:
                break

            # print(f'绘制新增bug增长曲线和关闭曲线，当前循环{index}, 值{i}, 值类型{type(i)}, str值{str(i)} ')
            startTime = bug_submit_date_list[index]
            endTime = bug_submit_date_list[index + 1]
            # print(f'起始时间{startTime}， 终止时间{endTime}，时间type{type(endTime)}')

            # 新增数 ，其实是查的一段时间内，提交过的bug数量，不是bugstatus=1 的数量
            # 第一个[startTime, endTime] 给add 用，第2个[startTime, endTime] 给add12 用，第N个[startTime, endTime] 给where参数 用，
            sqlargs = [startTime, endTime, startTime, endTime, startTime, endTime]  # list，有几个developer 填几套startTime, endTime
            for developer in developer_tuple:
                sqlargs.append(startTime)
                sqlargs.append(endTime)

            cursor.execute(search_sql, sqlargs)
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果, 包括：时间,项目，新增，关闭，开发0，开发0新增，开发0关闭，开发1。。。。
            sql_return_result_tuple = cursor.fetchall()
            print(f'开发维度，按时间（时间可自定义）统计全部 && 12级bug、关闭bug、待回归bug等 ，返回结果=={sql_return_result_tuple}')

            # 3. 解析结果，加入到bugcount list表中，每次只返回一条数据所以不用for循环了

            bug = dict()
            print(f'开发维度，按时间（时间可自定义）统计全部 && 12级bug、关闭bug、待回归bug等,tuple[0]', sql_return_result_tuple[0])
            print(f'开发维度，按时间（时间可自定义）统计全部 && 12级bug、关闭bug、待回归bug等,tuple[0][0]', sql_return_result_tuple[0][0])
            print(f'开发维度，按时间（时间可自定义）统计全部 && 12级bug、关闭bug、待回归bug等,tuple[0][1]', sql_return_result_tuple[0][1])
            bug['bug_submit_date'] = str(endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['project'] = sql_return_result_tuple[0][1]  # 项目名称
            bug['add'] = sql_return_result_tuple[0][2]  # 新增
            bug['close'] = sql_return_result_tuple[0][3]  # 关闭
            bug['regression'] = sql_return_result_tuple[0][4]  # 回归
            bug['delay'] = sql_return_result_tuple[0][5]  # 延迟
            bug['add12'] = sql_return_result_tuple[0][6]  # 新增(1-2级)
            bug['close12'] = sql_return_result_tuple[0][7]  # 关闭(1-2级)
            bug['regression12'] = sql_return_result_tuple[0][8]  # 回归(1-2级)
            bug['delay12'] = sql_return_result_tuple[0][9]  # 延迟(1-2级)
            bug['total12'] = sql_return_result_tuple[0][10]  # 总数(1-2级)
            # bug解决率有可能出现none的情况
            if sql_return_result_tuple[0][11] is None:
                bug['bug_close_rate'] = float(0)
            else:
                bug['bug_close_rate'] = float(sql_return_result_tuple[0][11])  #bug解决率


            # bug['rank'] = sql_return_result_tuple[0][12]  # 排名不是从数据库读出来的，而是自己算出来的
            bug['totalNum'] = sql_return_result_tuple[0][12]  # 总数
            bug['last'] = int(bug['totalNum']) - int(bug['close'])   # 剩余情况自己算的

            # 后面是项目相关的 关闭情况，有几个项目循环几次
            for developer in developer_tuple:

                # 当前索引
                # print(f'当前 developer r=={str(developer)}')
                index = developer_tuple.index(developer)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中 project 名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中 project 名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer))-3]  # 项目名称并不是从sql语句中读出来的，而是单独查询project sql语句中读出
                bug['add_developer' + str(index)] = sql_return_result_tuple[0][13 + 6*index + 1]
                bug['close_developer' + str(index)] = sql_return_result_tuple[0][13 + 6*index + 2]
                bug['regression_developer' + str(index)] = sql_return_result_tuple[0][13 + 6*index + 3]
                bug['delay_developer' + str(index)] = sql_return_result_tuple[0][13 + 6*index + 4]
                bug['total_developer' + str(index)] = sql_return_result_tuple[0][13 + 6*index + 5]
                bug['last_developer' + str(index)] = int(bug['total_developer' + str(index)]) - int(bug['close_developer' + str(index)])

                # print(f'developer{index}=', bug['developer' + str(index)])  #
                # print(f'add_developer{index}=', bug['add_developer' + str(index)])
                # print(f'close_developer{index} ==', bug['close_developer' + str(index)])

                # print(f'第{index}次循环结束================================================')

            print(f'开发维度，按时间（时间可自定义）统计全部 / 12 bug、关闭bug、待回归bug等,bug===={bug}')
            bugcount.append(bug)
            # for end

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


    #     按顺序执行完，就认为成功了
    code = 200
    msg = 'sql语句执行成功'
    count = len(bugcount)


    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist.py> ,开发维度每日数据，按时间（时间可自定义）统计全部  12 bug==jsonStr=====', json_str)

    print('=================================开发维度，按时间（时间可自定义）统计全部  12 bug、关闭bug、待回归bug等 end ===================================')
    return json_str

# ####################### 开发维度 start####################################
# 8) 开发维度，获取所有开发的 获取all bug 一段时间内的增长和关闭情况，为了画折线图project0 - project13(默认给13个开发，没有值默认不返回数据, ！！ 有几个开发返回几个开发的值)
def get_alldeveloperdata_withdeveloper_alongtime_allbug_orderby_date(startTime, endTime, timeDifference):
    print(
        '=================================获取all bug 一段时间内的增长和关闭情况 start ===================================')
    print('只需要返回新增/关闭/剩余 开发0新增/开发0关闭/开发0剩余 ')
    print(
        f'<app.py> get_alldeveloperdata_withdeveloper_alongtime_allbug_orderby_date, 传的参数{startTime}， {endTime}, {timeDifference}，类型{type(startTime)}， {type(endTime)}, {type(timeDifference)}')

    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    # 0. 先获取有多少个开发///////////////////////////////////////////////
    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个developer
        get_developer_sql = 'select developer from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and developer != "" group by developer'
        cursor.execute(get_developer_sql, [startTime, endTime])
        conn.commit()
        #     获取developer tuple
        developer_tuple = cursor.fetchall()

        # 2.获取有多少时间点 list
        bug_submit_date_list = utils.get_bug_submit_date_list(startTime, endTime, timeDifference)
        print('获取时间列表 bug_submit_date_list', bug_submit_date_list)
        # print('获取时间列表。type bug_submit_date_list.type = ', type(bug_submit_date_list))

        # 3.循环执行sql语句,获取bug_submit_date_list 中时间节点的数据

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project," \
                                 "count(bugid or null) as 'add', " \
                                 "count(bug_status = 2 or null) as 'close'," \
                                 "count(bug_status = 3 or null) as 'regression', " \
                                 "count(bug_status = 4 or null) as 'delay', " \
                                 "count(severity_level <= 2 or null) as 'add12', " \
                                 "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                 "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                 "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                 "count(severity_level <= 2 or null) as 'total12', " \
                                 "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                 "count(bugid or null) as 'totalNum' "

        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )"

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            # print(f'当前developer=={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str) - 2]
            # print('循环中的开发名str==', developer_name)

            # print(f'当前第{index}项 循环：第{index}开发为', developer_name)
            # print('拼接sql语句')
            # count(developer='1808' or null) as 'totalNumBydeveloperBelongdeveloper0',
            # 依次为开发1 / 属于开发1的全部bug / 属于开发1的新增bug / 属于开发1的关闭bug

            # developer='1808' as developer0
            sql_name_developer = ",developer=" + developer_name + "as developer" + str(index)
            # print('name ==========', sql_name_developer)

            sql_add_num_bydeveloper_belong_developer = ",count(developer = " + developer_name + "or null) as add_num_developer" + str(index)
            sql_close_num_bydeveloper_belong_developer = ",count(bug_status=2 and developer = " + developer_name + "or null) as close_num_developer" + str(index)
            sql_regression_num_bydeveloper_belong_developer = ",count(bug_status=3 and developer = " + developer_name + "or null) as regression_num_developer" + str(index)
            sql_delay_num_bydeveloper_belong_developer = ",count(bug_status=4 and developer = " + developer_name + "or null) as delay_num_developer" + str(index)
            sql_total_num_bydeveloper_belong_developer = ",count(developer = " + developer_name + "or null) as total_num_developer" + str(index)
            """
            print('for 循环拼接的sql == ', sql_name_developer + sql_add_num_bydeveloper_belong_developer +sql_close_num_bydeveloper_belong_developer +
                  sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer)
            """
            for_sql = sql_name_developer + sql_add_num_bydeveloper_belong_developer + sql_close_num_bydeveloper_belong_developer + sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer + sql_total_num_bydeveloper_belong_developer
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            # print('开发相关sql 拼接结果==', search_sql_middle_about_developer)

        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_developer + searchsql_end
        print(f'开发维度，查询allbug 最终查询sql ==={search_sql}')  # 开发名称并不是从sql语句中读出来的，而是单独查询developer sql语句中读出

        # 2. 获取数据，定义累加参数
        closenum_developer = 0  # 开发维度累计关闭
        lastnum_developer = 0  # 开发维度 累计剩余
        close12num_developer = 0  # 开发维度 累计12级关闭
        sum_args_developer_dict = dict()
        for developer in developer_tuple:
            # 当前索引
            index = developer_tuple.index(developer)
            sum_args_developer_dict['closenum_developer' + str(index)] = 0
            sum_args_developer_dict['lastnum_developer' + str(index)] = 0  # 定义累计剩余情况


        for developer in developer_tuple:
            # 当前索引
            print(f'当前 developer r=={str(developer)}')
        #  for 执行sql语句,查出结果，循环len(bug_submit_date_list) -1 次,从list取出来直接str设备
        for i in bug_submit_date_list:
            index = bug_submit_date_list.index(i)
            if index == len(bug_submit_date_list) - 1:
                break

            # print(f'绘制新增bug增长曲线和关闭曲线，当前循环{index}, 值{i}, 值类型{type(i)}, str值{str(i)} ')
            startTime = bug_submit_date_list[index]
            # 绘制累计关闭的开始时间 从最早开始算
            startTimeSumClose = bug_submit_date_list[0]
            endTime = bug_submit_date_list[index + 1]
            # print(f'起始时间{startTime}， 终止时间{endTime}，时间type{type(endTime)}')

            # 新增数 ，其实是查的一段时间内，提交过的bug数量，不是bugstatus=1 的数量
            # # 第一个[startTime, endTime] 给add 用，第2个[startTime, endTime] 给add12 用，第N个[startTime, endTime] 给where参数 用，
            # sqlargs = [startTime, endTime, startTimeSumClose, endTime]  #不分开发情况下的 add close
            #
            # # list，有几个developer 填几套startTime, endTime
            # for developer in developer_tuple:
            #     sqlargs.append(startTime)
            #     sqlargs.append(endTime)
            # [startTime, endTime]  # 这是最后 一个时间where startTime >= xxx and endTime <= xxx


            cursor.execute(search_sql, [startTime, endTime])
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果, 包括：时间,开发，新增，关闭，开发0，开发0新增，开发0关闭，开发1。。。。
            sql_return_result_tuple = cursor.fetchall()
            print(f'绘制新增bug增长曲线和关闭曲线，返回结果=={sql_return_result_tuple}')

            # 3. 解析结果，加入到bugcount list表中，每次只返回一条数据所以不用for循环了

            bug = dict()
            print(f'绘制新增bug增长曲线和关闭曲线,tuple[0]', sql_return_result_tuple[0])
            print(f'绘制新增bug增长曲线和关闭曲线,tuple[0][0]', sql_return_result_tuple[0][0])
            print(f'绘制新增bug增长曲线和关闭曲线,tuple[0][1]', sql_return_result_tuple[0][1])
            bug['bug_submit_date'] = str(endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['project'] = sql_return_result_tuple[0][1]  # 项目名称
            bug['add'] = sql_return_result_tuple[0][2]  # 新增
            closenum_developer += sql_return_result_tuple[0][3]
            bug['close'] = closenum_developer  # 累计关闭，目前是查出来 时间颗粒度 这段时间的close
            bug['regression'] = sql_return_result_tuple[0][4]  # 回归
            bug['delay'] = sql_return_result_tuple[0][5]  # 延迟
            bug['add12'] = sql_return_result_tuple[0][6]  # 新增(1-2级)

            close12num_developer += sql_return_result_tuple[0][7]
            bug['close12'] = close12num_developer  # 累计 关闭(1-2级)
            bug['regression12'] = sql_return_result_tuple[0][8]  # 回归(1-2级)
            bug['delay12'] = sql_return_result_tuple[0][9]  # 延迟(1-2级)
            bug['total12'] = sql_return_result_tuple[0][10]  # 总数(1-2级)
            # bug解决率有可能出现none的情况
            if sql_return_result_tuple[0][11] is None:
                bug['bug_close_rate'] = float(0)
            else:
                bug['bug_close_rate'] = float(sql_return_result_tuple[0][11])  # bug解决率

            # bug['rank'] = sql_return_result_tuple[0][12]  # 排名不是从数据库读出来的，而是自己算出来的
            bug['totalNum'] = sql_return_result_tuple[0][12]  # 总数

            lastnum_developer += int(bug['totalNum']) - int(sql_return_result_tuple[0][3])  # 剩余情况自己算的-算一个累计的情况
            bug['last'] = lastnum_developer

            # 后面是开发相关的 关闭情况，有几个开发循环几次
            for developer in developer_tuple:
                # 当前索引
                # print(f'当前 developer r=={str(developer)}')
                index = developer_tuple.index(developer)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中 developer 名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中 developer 名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer)) - 3]  # 开发名称并不是从sql语句中读出来的，而是单独查询developer sql语句中读出
                bug['add_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 1]

                sum_args_developer_dict['closenum_developer' + str(index)] += sql_return_result_tuple[0][13 + 6 * index + 2]
                bug['close_developer' + str(index)] = sum_args_developer_dict['closenum_developer' + str(index)]  # 累计关闭
                bug['regression_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 3]
                bug['delay_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 4]
                bug['total_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 5]
                sum_args_developer_dict['lastnum_developer' + str(index)] += int(bug['total_developer' + str(index)]) - int(sql_return_result_tuple[0][13 + 6 * index + 2])
                bug['last_developer' + str(index)] = sum_args_developer_dict['lastnum_developer' + str(index)]

                # print(f'developer{index}=', bug['developer' + str(index)])  #
                # print(f'add_developerr{index}=', bug['add_developer' + str(index)])
                # print(f'close_developerr{index} ==', bug['close_developer' + str(index)])

                # print(f'第{index}次循环结束================================================')

            print(f'绘制新增bug增长曲线和关闭曲线,bug===={bug}')
            bugcount.append(bug)
            # for end

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

    #     按顺序执行完，就认为成功了
    code = 200
    msg = 'sql语句执行成功'
    count = len(bugcount)

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print(
        '<buglist> ,get_alldeveloperdata_withdeveloper_everyday_newbug_addandclose_orderby_date,获取新增bug(status=1) 今天相对昨天的增长和关闭情返回结果==jsonStr=====',
        json_str)

    print('=================================获取all bug 一段时间内的增长和关闭情况 end ===================================')
    return json_str


# 7）开发维度，按时间（时间可自定义），按照一定时间颗粒度（时间可自定义），绘制新增bug增长曲线和关闭曲线；，为了画折线图project0 - project13(默认给13个开发，没有值默认不返回数据, ！！ 有几个开发返回几个开发的值)
def get_alldeveloperdata_withdeveloper_alongtime_addandclosebug_orderby_date(startTime, endTime, timeDifference):
    print(
        '=================================获取新增 bug 一段时间内的增长和关闭情况 start ===================================')
    print('只需要返回新增/关闭 开发0新增/开发0关闭 ')
    print(
        f'<app.py> get_alldeveloperdata_withdeveloper_alongtime_addandclosebug_orderby_date, 传的参数{startTime}， {endTime}, {timeDifference}，类型{type(startTime)}， {type(endTime)}, {type(timeDifference)}')

    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    # 0. 先获取有多少个开发///////////////////////////////////////////////
    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数
        # 1. 获取有几个developer
        get_developer_sql = 'select developer from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and developer != "" group by developer'
        cursor.execute(get_developer_sql, [startTime, endTime])
        conn.commit()
        #     获取developer tuple
        developer_tuple = cursor.fetchall()

        # 2.获取有多少时间点 list
        bug_submit_date_list = utils.get_bug_submit_date_list(startTime, endTime, timeDifference)
        print('获取时间列表 bug_submit_date_list', bug_submit_date_list)
        # print('获取时间列表。type bug_submit_date_list.type = ', type(bug_submit_date_list))

        # 3.循环执行sql语句,获取bug_submit_date_list 中时间节点的数据

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project," \
                                 "count(bugid or null) as 'add', " \
                                 "count(bug_status = 2 or null) as 'close'," \
                                 "count(bug_status = 3 or null) as 'regression', " \
                                 "count(bug_status = 4 or null) as 'delay', " \
                                 "count(severity_level <= 2 or null) as 'add12', " \
                                 "count(bug_status = 2 and severity_level <= 2 or null) as 'close12', " \
                                 "count(bug_status = 3 and severity_level <= 2 or null) as 'regression12', " \
                                 "count(bug_status = 4 and severity_level <= 2 or null) as 'delay12', " \
                                 "count(severity_level <= 2 or null) as 'total12', " \
                                 "convert( count(bug_status = 2 or null)/count(bugid or null),decimal(10,2) ) as 'rate', " \
                                 "count(bugid or null) as 'totalNum' "

        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )"

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            # print(f'当前developer=={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str) - 2]
            # print('循环中的开发名str==', developer_name)

            # print(f'当前第{index}项 循环：第{index}开发为', developer_name)
            # print('拼接sql语句')
            # count(developer='1808' or null) as 'totalNumBydeveloperBelongdeveloper0',
            # 依次为开发1 / 属于开发1的全部bug / 属于开发1的新增bug / 属于开发1的关闭bug

            # developer='1808' as developer0
            sql_name_developer = ",developer=" + developer_name + "as developer" + str(index)
            # print('name ==========', sql_name_developer)

            sql_add_num_bydeveloper_belong_developer = ",count(developer = " + developer_name + " or null) as add_num_developer" + str(index)
            sql_close_num_bydeveloper_belong_developer = ",count(bug_status=2 and developer = " + developer_name + " or null) as close_num_developer" + str(index)
            sql_regression_num_bydeveloper_belong_developer = ",count(bug_status=3 and developer = " + developer_name + " or null) as regression_num_developer" + str(index)
            sql_delay_num_bydeveloper_belong_developer = ",count(bug_status=4 and developer = " + developer_name + " or null) as delay_num_developer" + str(index)
            sql_total_num_bydeveloper_belong_developer = ",count(developer = " + developer_name + " or null) as total_num_developer" + str(index)
            """
            print('for 循环拼接的sql == ', sql_name_developer + sql_add_num_bydeveloper_belong_developer +sql_close_num_bydeveloper_belong_developer +
                  sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer)
            """
            for_sql = sql_name_developer + sql_add_num_bydeveloper_belong_developer + sql_close_num_bydeveloper_belong_developer + sql_regression_num_bydeveloper_belong_developer + sql_delay_num_bydeveloper_belong_developer + sql_total_num_bydeveloper_belong_developer
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            # print('开发相关sql 拼接结果==', search_sql_middle_about_developer)

        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_developer + searchsql_end
        print(f'开发维度，查询allbug 最终查询sql ==={search_sql}')  # 开发名称并不是从sql语句中读出来的，而是单独查询developer sql语句中读出

        # 2. 获取数据，定义累加参数
        closenum_developer = 0  # 开发维度累计关闭
        lastnum_developer = 0  # 开发维度 累计剩余
        close12num_developer = 0  # 开发维度 累计12级关闭
        sum_args_developer_dict = dict()
        for developer in developer_tuple:
            # 当前索引
            index = developer_tuple.index(developer)
            sum_args_developer_dict['closenum_developer' + str(index)] = 0
            sum_args_developer_dict['lastnum_developer' + str(index)] = 0  # 定义累计剩余情况

        #  for 执行sql语句,查出结果，循环len(bug_submit_date_list) -1 次,从list取出来直接str设备
        for i in bug_submit_date_list:
            index = bug_submit_date_list.index(i)
            if index == len(bug_submit_date_list) - 1:
                break
            # print(f'绘制新增bug增长曲线和关闭曲线，当前循环{index}, 值{i}, 值类型{type(i)}, str值{str(i)} ')
            startTime = bug_submit_date_list[index]
            # 绘制累计关闭的开始时间 从最早开始算
            startTimeSumClose = bug_submit_date_list[0]
            endTime = bug_submit_date_list[index + 1]
            # print(f'起始时间{startTime}， 终止时间{endTime}，时间type{type(endTime)}')

            # 新增数 ，其实是查的一段时间内，提交过的bug数量，不是bugstatus=1 的数量
            # # 第一个[startTime, endTime] 给add 用，第2个[startTime, endTime] 给add12 用，第N个[startTime, endTime] 给where参数 用，
            # sqlargs = [startTime, endTime, startTimeSumClose, endTime]  #不分开发情况下的 add close
            #
            # # list，有几个developer 填几套startTime, endTime
            # for developer in developer_tuple:
            #     sqlargs.append(startTime)
            #     sqlargs.append(endTime)
            # [startTime, endTime]  # 这是最后 一个时间where startTime >= xxx and endTime <= xxx


            cursor.execute(search_sql, [startTime, endTime])
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果, 包括：时间,开发，新增，关闭，开发0，开发0新增，开发0关闭，开发1。。。。
            sql_return_result_tuple = cursor.fetchall()
            print(f'绘制新增bug增长曲线和关闭曲线，返回结果=={sql_return_result_tuple}')

            # 3. 解析结果，加入到bugcount list表中，每次只返回一条数据所以不用for循环了

            bug = dict()
            print(f'绘制新增bug增长曲线和关闭曲线,tuple[0]', sql_return_result_tuple[0])
            print(f'绘制新增bug增长曲线和关闭曲线,tuple[0][0]', sql_return_result_tuple[0][0])
            print(f'绘制新增bug增长曲线和关闭曲线,tuple[0][1]', sql_return_result_tuple[0][1])
            bug['bug_submit_date'] = str(endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            bug['project'] = sql_return_result_tuple[0][1]  # 项目名称
            bug['add'] = sql_return_result_tuple[0][2]  # 新增，时间颗粒度 这段时间的add
            closenum_developer += sql_return_result_tuple[0][3]
            bug['close'] = sql_return_result_tuple[0][3]  # 关闭， 时间颗粒度 这段时间的close
            bug['regression'] = sql_return_result_tuple[0][4]  # 回归
            bug['delay'] = sql_return_result_tuple[0][5]  # 延迟
            bug['reopen'] = sql_return_result_tuple[0][5]  # 重开

            bug['add12'] = sql_return_result_tuple[0][6]  # 新增(1-2级)
            close12num_developer += sql_return_result_tuple[0][7]
            bug['close12'] = close12num_developer  # 累计 关闭(1-2级)
            bug['regression12'] = sql_return_result_tuple[0][8]  # 回归(1-2级)
            bug['delay12'] = sql_return_result_tuple[0][9]  # 延迟(1-2级)
            bug['total12'] = sql_return_result_tuple[0][10]  # 总数(1-2级)
            # bug解决率有可能出现none的情况
            if sql_return_result_tuple[0][11] is None:
                bug['bug_close_rate'] = float(0)
            else:
                bug['bug_close_rate'] = float(sql_return_result_tuple[0][11])  # bug解决率

            # bug['rank'] = sql_return_result_tuple[0][12]  # 排名不是从数据库读出来的，而是自己算出来的
            bug['totalNum'] = sql_return_result_tuple[0][12]  # 总数

            lastnum_developer += int(bug['totalNum']) - int(sql_return_result_tuple[0][3])  # 剩余情况自己算的-算一个累计的情况
            bug['last'] = lastnum_developer

            # 后面是开发相关的 关闭情况，有几个开发循环几次
            for developer in developer_tuple:
                # 当前索引
                # print(f'当前 developer r=={str(developer)}')
                index = developer_tuple.index(developer)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中 developer 名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中 developer 名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer)) - 3]  # 开发名称并不是从sql语句中读出来的，而是单独查询developer sql语句中读出
                bug['add_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 1]

                sum_args_developer_dict['closenum_developer' + str(index)] += sql_return_result_tuple[0][13 + 6 * index + 2]
                bug['close_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 2]  # 关闭,时间颗粒度 这段时间的close
                bug['regression_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 3]
                bug['delay_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 4]
                bug['total_developer' + str(index)] = sql_return_result_tuple[0][13 + 6 * index + 5]
                sum_args_developer_dict['lastnum_developer' + str(index)] += int(bug['total_developer' + str(index)]) - int(sql_return_result_tuple[0][13 + 6 * index + 2])
                bug['last_developer' + str(index)] = int(bug['total_developer' + str(index)]) - int(sql_return_result_tuple[0][13 + 6 * index + 2])  # 剩余,时间颗粒度 这段时间的close

                # print(f'developer{index}=', bug['developer' + str(index)])  #
                # print(f'add_developerr{index}=', bug['add_developer' + str(index)])
                # print(f'close_developerr{index} ==', bug['close_developer' + str(index)])

                # print(f'第{index}次循环结束================================================')

            print(f'绘制新增bug增长曲线和关闭曲线,bug===={bug}')
            bugcount.append(bug)
            # for end

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

    #     按顺序执行完，就认为成功了
    code = 200
    msg = 'sql语句执行成功'
    count = len(bugcount)

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = bugcount

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print(
        '<buglist> ,get_alldeveloperdata_withdeveloper_alongtime_addandclosebug_orderby_date,获取新增 今天相对昨天的增长和关闭情返回结果==jsonStr=====',
        json_str)

    print('=================================获取new bug 一段时间内的增长和关闭情况 end ===================================')
    return json_str


# 9）开发维度，按时间（时间可自定义）统计软件自测考量：相比较这段时间产生的所有bug，易bug产生比率；
def get_easybug_table_withdeveloper_orderby_date(startTime, endTime):
    print('=================================获取所有 开发维度 易bug产生比率 的数据 start ===================================')
    print(f'app.py 传的参数{startTime}， {endTime}')

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数

        # 1. 获取有几个 developer
        get_developer_sql = 'select developer from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) group by developer'
        cursor.execute(get_developer_sql, [startTime, endTime])
        conn.commit()
        #     获取 developer tuple
        developer_tuple = cursor.fetchall()

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project," \
                                 "convert( count(bug_difficulty = 2 or null)/count(bugid or null),decimal(10,2) ) as 'easybug_rate' " \

        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )"
        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        search_sql_args = list()
        # print('未拼接好的字符串==', searchsql_not_complete + searchsql_end)

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            # print(f'当前 developer =={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str) - 2]
            # print('循环中的 developer 名str==', developer_name)

            # print(f'当前第{index}项 循环：第{index}项目为', developer_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为开发1 / 属于开发1的全部bug / 属于开发1的新增bug / 属于开发1的关闭bug

            # project='1808' as project0
            sql_name_developer = ",developer=" + developer_name + " as developer" + str(index)
            # print('name ==========', sql_name_developer)
            # 执行到这没问题

            # sql_easybug_rate_belong_developer = ", count(bug_difficulty = 2 and developer = " + developer_name + " or null) as easybug_rate_developer" + str(index)
            sql_easybug_rate_belong_developer = ", convert( count(bug_difficulty = 2 and developer = " + developer_name + " or null)/count(bugid or null),decimal(10,2) ) as easybug_rate_developer" + str(index)
            # print('for 循环拼接的sql == ', sql_easybug_rate_belong_developer)

            for_sql = sql_easybug_rate_belong_developer
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            # print('开发相关sql 拼接结果==', search_sql_middle_about_developer)

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
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        # print("sql语句执行成功")

        rank = 1  # 排名
        # 3. 整理返回给前端的值,相当于按时间循环
        # 返回数据 第几行 第几列xx数据
        for r in sql_return_result_tuple:
            # print('=======================r=', r)

            bug = dict()
            bug['bug_submit_date'] = str(startTime + ' - ' + endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            # print('========================bug_submit_date', bug['bug_submit_date'])
            bug['project'] = r[1]  # 项目名称
            # bug解决率有可能出现none的情况
            if r[2] is None:
                bug['easy_bug_rate'] = str((float(0) * 100)) + '%'  # 易bug比率
            else:
                bug['easy_bug_rate'] = str((float(r[2]) * 100)) + '%'  # 易bug比率
            # bug['easy_bug_rate'] = str((float(r[2]) * 100)) + '%'  # 易bug比率

            # 后面是项目相关的 ，有几个项目循环几次
            for developer in developer_tuple:
                # 当前索引
                # print(f'当前developer=={str(developer)}')
                index = developer_tuple.index(developer)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中developer名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中developer名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer)) - 3]  # 项目名称并不是从sql语句中读出来的，developer sql语句中读出
                # bug解决率有可能出现none的情况
                if r[3 + index] is None:
                    bug['easy_bug_rate'] = str((float(0) * 100)) + '%'  # 易bug比率
                else:
                    bug['easy_bug_rate'] = str((float(r[3 + index]) * 100)) + '%'  # 易bug比率
                # bug['easy_bug_rate_developer' + str(index)] = str((float(r[3 + index]) * 100)) + '%'

                # print(f'developer{index}=', bug['developer' + str(index)])  #
                # print(f'add_developer{index}=', bug['add_developer' + str(index)])
                # print(f'close_developer{index} ==', bug['close_developer' + str(index)])
                # print(f'regression_developer{index}  ===', bug['regression_developer' + str(index)])
                # print(f'delay_developer{index}  ===', bug['delay_developer' + str(index)])
                #
                # print(f'第{index}次循环结束================================================')

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
    print('<admin.py> 搜索易bug产生比率 type(data)== ', type(data))
    print('<admin.py> 搜索易bug产生比率 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist> get_easybug_table_withdeveloper_orderby_date,返回结果==jsonStr=====', json_str)

    print('=================================获取所有 开发维度 易bug产生比率 的数据 end ===================================')
    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str


# 11）开发维度，按时间（时间可自定义），按照一定时间颗粒度（时间可自定义），绘制易bug产生比率曲线；1/2    月/周/季
def get_easybug_table_fordrawmap_withdeveloper_orderby_date(startTime, endTime, timeDifference):
    print('=================================获取所有 开发维度,一定时间颗粒度,易bug产生比率 的数据 start ===================================')
    print(f'app.py 传的参数timeDifference {startTime}， {endTime}, {timeDifference}')

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数

        # 1. 获取有几个 developer
        get_developer_sql = 'select developer from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and developer != "" group by developer'
        cursor.execute(get_developer_sql, [startTime, endTime])
        conn.commit()
        #     获取 developer tuple
        developer_tuple = cursor.fetchall()

        # 2.获取有多少时间点 list
        bug_submit_date_list = utils.get_bug_submit_date_list(startTime, endTime, timeDifference)
        print('获取时间列表 bug_submit_date_list', bug_submit_date_list)
        # print('获取时间列表。type bug_submit_date_list.type = ', type(bug_submit_date_list))

        # 1. 拼接sql查询语句
        searchsql_not_complete = "select bug_submit_date, project," \
                                 "convert( count(bug_difficulty = 2 or null)/count(bugid or null),decimal(10,2) ) as 'easybug_rate' " \

        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s )"
        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        search_sql_args = list()
        # print('未拼接好的字符串==', searchsql_not_complete + searchsql_end)

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            # print(f'当前 developer =={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str) - 2]
            # print('循环中的 developer 名str==', developer_name)

            # print(f'当前第{index}项 循环：第{index}项目为', developer_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为开发1 / 属于开发1的全部bug / 属于开发1的新增bug / 属于开发1的关闭bug

            # project='1808' as project0
            sql_name_developer = ",developer=" + developer_name + " as developer" + str(index)
            # print('name ==========', sql_name_developer)
            # 执行到这没问题

            # sql_easybug_rate_belong_developer = ", count(bug_difficulty = 2 and developer = " + developer_name + " or null) as easybug_rate_developer" + str(index)
            sql_easybug_rate_belong_developer = ", convert( count(bug_difficulty = 2 and developer = " + developer_name + " or null)/count(bugid or null),decimal(10,2) ) as easybug_rate_developer" + str(index)
            # print('for 循环拼接的sql == ', sql_easybug_rate_belong_developer)

            for_sql = sql_easybug_rate_belong_developer
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            # print('开发相关sql 拼接结果==', search_sql_middle_about_developer)

        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_developer + searchsql_end
        print('最终sql ==', search_sql)



        rank = 1  # 排名
        # 3. 整理返回给前端的值,相当于按时间循环
        # 返回数据 第几行 第几列xx数据
        for r in bug_submit_date_list:
            # print('=======================r=', r)
            index = bug_submit_date_list.index(r)
            if index == len(bug_submit_date_list) - 1:
                break

            # print(f'按照一定时间颗粒度（时间可自定义），绘制易bug产生比率曲线，当前循环{index}, 值{i}, 值类型{type(i)}, str值{str(i)} ')
            startTime = bug_submit_date_list[index]
            endTime = bug_submit_date_list[index + 1]
            # print(f'起始时间{startTime}， 终止时间{endTime}，时间type{type(endTime)}')

            # 2. 执行sql语句
            cursor.execute(search_sql, [startTime, endTime])
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果
            sql_return_result_tuple = cursor.fetchall()

            # 转换查询结果为[{},{},{}]这种格式的
            # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
            # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
            # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
            # print("sql语句执行成功")

            bug = dict()
            # bug['bug_submit_date'] = str(startTime + ' - ' + endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable （xx -xx 这种格式）
            bug['bug_submit_date'] = str(endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            # print('========================bug_submit_date', bug['bug_submit_date'])
            bug['project'] = r[1]  # 项目名称
            # bug解决率有可能出现none的情况
            if sql_return_result_tuple[0][2] is None:
                # bug['easy_bug_rate'] = str((float(0) * 100)) + '%'  # 易bug比率
                bug['easy_bug_rate'] = float(0)  # 易bug比率
            else:
                bug['easy_bug_rate'] = float(sql_return_result_tuple[0][2]) * 100 # 易bug比率

            # bug['easy_bug_rate'] = str((float(sql_return_result_tuple[0][2]) * 100)) + '%'  # 易bug比率

            # 后面是项目相关的 ，有几个项目循环几次
            for developer in developer_tuple:
                # 当前索引
                # print(f'当前developer=={str(developer)}')
                index = developer_tuple.index(developer)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中developer名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中developer名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer)) - 3]  # 项目名称并不是从sql语句中读出来的，developer sql语句中读出
                # bug解决率有可能出现none的情况
                if sql_return_result_tuple[0][3 + index] is None:
                    # bug['easy_bug_rate_developer' + str(index)] = str((float(0) * 100)) + '%'  # 易bug比率
                    bug['easy_bug_rate_developer' + str(index)] = float(0) * 100  # 易bug比率
                else:
                    # bug['easy_bug_rate_developer' + str(index)] = str((float(sql_return_result_tuple[0][3 + index]) * 100)) + '%'  # 易bug比率
                    bug['easy_bug_rate_developer' + str(index)] = float(sql_return_result_tuple[0][3 + index]) * 100  # 易bug比率
                # bug['easy_bug_rate_developer' + str(index)] = str((float(sql_return_result_tuple[0][3 + index]) * 100)) + '%'

                # print(f'developer{index}=', bug['developer' + str(index)])  #
                # print(f'add_developer{index}=', bug['add_developer' + str(index)])
                # print(f'close_developer{index} ==', bug['close_developer' + str(index)])
                # print(f'regression_developer{index}  ===', bug['regression_developer' + str(index)])
                # print(f'delay_developer{index}  ===', bug['delay_developer' + str(index)])
                #
                # print(f'第{index}次循环结束================================================')

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
    print('<admin.py> 搜索易bug产生比率 type(data)== ', type(data))
    print('<admin.py> 搜索易bug产生比率 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist> get_easybug_table_withdeveloper_orderby_date,返回结果==jsonStr=====', json_str)

    print('=================================获取所有 开发维度,一定时间颗粒度,易bug产生比率 的数据 的数据 end ===================================')
    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str


# 10）开发维度，按时间（时间可自定义）统计bug解决的及时性考量：一二级bug一定时间内（可自定义）的解决率，三四级bug一定时间内（可自定义时间）
def get_bugsolverate_table_fordrawmap_withdeveloper_orderby_date(startTime, endTime, timeDifference):
    print('=================================获取所有 开发维度,一定时间颗粒度,bug解决率(12 -34) 的数据 start ===================================')
    print(f'app.py 传的参数timeDifference {startTime}， {endTime}, {timeDifference}')

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    # json数据
    data = {}
    bugcount = []
    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败，此时间范围内无数据'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 拿到各种想要的参数

        # 1. 获取有几个 developer
        get_developer_sql = 'select developer from bugcount.buglist where (bug_submit_date >= %s and  bug_submit_date <= %s ) and developer != "" group by developer'
        cursor.execute(get_developer_sql, [startTime, endTime])
        conn.commit()
        #     获取 developer tuple
        developer_tuple = cursor.fetchall()

        # 2.获取有多少时间点 list
        bug_submit_date_list = utils.get_bug_submit_date_list(startTime, endTime, timeDifference)
        print('获取时间列表 bug_submit_date_list', bug_submit_date_list)
        # print('获取时间列表。type bug_submit_date_list.type = ', type(bug_submit_date_list))

        # 1. 拼接sql查询语句 --比如一周，bug应该关闭时间在endtime 之前的
        """
        searchsql_not_complete = "select bug_submit_date, project," \
                                 " convert( (count(bug_status = 2 and date_add(bug_submit_date, interval %s day) between %s and %s or null))/(count(date_add(bug_submit_date, interval %s day) between %s and %s or null)),decimal(10,2) ) as 'bug_solve_rate' "
        """
        searchsql_not_complete = "select bug_submit_date, project, " \
                                 " convert( (count(severity_level <= 2 and bug_status = 2 and date_add(bug_submit_date, interval %s day) between %s and %s or null))/(count(severity_level <= 2 and  date_add(bug_submit_date, interval %s day) between %s and %s or null)),decimal(10,2) ) as 'bug_solve_rate' " \
                                 ", convert( (count(severity_level > 2 and bug_status = 2 and date_add(bug_submit_date, interval %s day) between %s and %s or null))/(count(severity_level > 2 and  date_add(bug_submit_date, interval %s day) between %s and %s or null)),decimal(10,2) ) as 'bug_solve_rate' "

        # date_add(bug_submit_date, interval 7 day) <=%s <= endTime(最后一个时间) severity_level
        searchsql_end = " from bugcount.buglist where (bug_submit_date >= %s and bug_submit_date <= %s )"

        # 初始化 sqlc查询参数 total_roject0 add_project0 close_project0
        # "convert( count(date_add(bug_submit_date, interval 7 day) <= '2020-01-17' or null)/count(severity_level <=2 or null),decimal(10,2) ) as 'bug_solve_rate' "
        search_sql_args = list()
        # print('未拼接好的字符串==', searchsql_not_complete + searchsql_end)

        search_sql_middle_about_developer = ""
        # 循环拼接字符串
        for developer in developer_tuple:
            # 当前索引
            # print(f'当前 developer =={str(developer)}')
            index = developer_tuple.index(developer)
            developer_name_tuple_to_str = str(developer_tuple[index])
            developer_name = developer_name_tuple_to_str[1:len(developer_name_tuple_to_str) - 2]
            # print('循环中的 developer 名str==', developer_name)

            # print(f'当前第{index}项 循环：第{index}项目为', developer_name)
            # print('拼接sql语句')
            # count(project='1808' or null) as 'totalNumByProjectBelongProject0',
            # 依次为开发1 / 属于开发1的全部bug / 属于开发1的新增bug / 属于开发1的关闭bug

            # project='1808' as project0
            sql_name_developer = ",developer=" + developer_name + " as developer" + str(index)
            # print('name ==========', sql_name_developer)
            # 执行到这没问题

            # sql_bug_solve_rate_belong_developer = ", convert( count(bug_difficulty = 2 and developer = " + developer_name + " or null)/count(bugid or null),decimal(10,2) ) as easybug_rate_developer" + str(index)
            sql_bug12_solve_rate_belong_developer = ", convert( (count(severity_level <= 2 and bug_status = 2 and date_add(bug_submit_date, interval %s day) between %s and %s and developer = " + developer_name + " or null))/(count(severity_level <= 2 and  date_add(bug_submit_date, interval %s day) between %s and %s or null)),decimal(10,2) ) as bug12_solve_rate_developer" + str(index)
            sql_bug34_solve_rate_belong_developer = ", convert( (count(severity_level > 2 and bug_status = 2 and date_add(bug_submit_date, interval %s day) between %s and %s and developer = " + developer_name + " or null))/(count(severity_level > 2 and  date_add(bug_submit_date, interval %s day) between %s and %s or null)),decimal(10,2) ) as bug34_solve_rate_developer" + str(index)
            sql_bug_solve_rate_belong_developer = sql_bug12_solve_rate_belong_developer + sql_bug34_solve_rate_belong_developer
            # print('for 循环拼接的sql == ', sql_bug_solve_rate_belong_developer)

            for_sql = sql_bug_solve_rate_belong_developer
            # search_sql_middle_about_developer 基础上拼接
            search_sql_middle_about_developer += for_sql
            # print('开发相关sql 拼接结果==', search_sql_middle_about_developer)

        # for循环拼接sql end
        search_sql = searchsql_not_complete + search_sql_middle_about_developer + searchsql_end
        print('get_bugsolverate_table_fordrawmap_withdeveloper_orderby_date,最终sql ==', search_sql)



        rank = 1  # 排名
        # 3. 整理返回给前端的值,相当于按时间循环
        # 返回数据 第几行 第几列xx数据
        timeDifference_int = int(timeDifference)
        for r in bug_submit_date_list:
            # print('=======================r=', r)
            index = bug_submit_date_list.index(r)
            if index == len(bug_submit_date_list) - 1:
                break

            # print(f'按照一定时间颗粒度（时间可自定义），绘制易bug产生比率曲线，当前循环{index}, 值{i}, 值类型{type(i)}, str值{str(i)} ')
            startTime = bug_submit_date_list[index]
            endTime = bug_submit_date_list[index + 1]
            # print(f'起始时间{startTime}， 终止时间{endTime}，时间type{type(endTime)}')

            # 2. 执行sql语句
            start_time_add_timediffrence_date = datetime.datetime.strptime(startTime, '%Y-%m-%d')
            end_time_add_timediffrence_date = datetime.datetime.strptime(endTime, '%Y-%m-%d')
            delta = datetime.timedelta(days=int(timeDifference))
            
            start_time_add_timediffrence_str = datetime.datetime.strftime((start_time_add_timediffrence_date + delta), '%Y-%m-%d')
            end_time_add_timediffrence_str = datetime.datetime.strftime((end_time_add_timediffrence_date + delta), '%Y-%m-%d') # startTime+7/14/21/30
            sql_args = [timeDifference_int, start_time_add_timediffrence_str, end_time_add_timediffrence_str, timeDifference_int, start_time_add_timediffrence_str, end_time_add_timediffrence_str,
                        timeDifference_int, start_time_add_timediffrence_str, end_time_add_timediffrence_str, timeDifference_int, start_time_add_timediffrence_str, end_time_add_timediffrence_str]  # 第一行12级bug参数 第二行34级bug参数
            # 有几个developer就加几对参数
            for developer in developer_tuple:
                # 12级bug参数
                sql_args.append(timeDifference_int)
                sql_args.append(start_time_add_timediffrence_str)
                sql_args.append(end_time_add_timediffrence_str)  # 除数
                sql_args.append(timeDifference_int)
                sql_args.append(start_time_add_timediffrence_str)
                sql_args.append(end_time_add_timediffrence_str)   # 被除数
                # 34级bug参数
                sql_args.append(timeDifference_int)
                sql_args.append(start_time_add_timediffrence_str)
                sql_args.append(end_time_add_timediffrence_str)  # 除数
                sql_args.append(timeDifference_int)
                sql_args.append(start_time_add_timediffrence_str)
                sql_args.append(end_time_add_timediffrence_str)  # 被除数
            sql_args.append(startTime)  # 加最后时间
            sql_args.append(endTime)  # 加最后时间

            cursor.execute(search_sql, sql_args)
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果
            sql_return_result_tuple = cursor.fetchall()

            # 转换查询结果为[{},{},{}]这种格式的
            # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
            # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
            # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
            # print("sql语句执行成功")

            bug = dict()
            # bug['bug_submit_date'] = str(startTime + ' - ' + endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable （xx -xx 这种格式）
            bug['bug_submit_date'] = str(endTime)  # 时间格式，转成str 否则报错：TypeError: Object of type date is not JSON serializable
            # print('========================bug_submit_date', bug['bug_submit_date'])
            bug['project'] = r[1]  # 项目名称
            # bug解决率有可能出现none的情况
            if sql_return_result_tuple[0][2] is None:
                bug['bug12_solve_rate'] = float(0)  # bug12解决率
            else:
                bug['bug12_solve_rate'] = float(sql_return_result_tuple[0][2]) * 100  # bug12解决率

            if sql_return_result_tuple[0][3] is None:
                bug['bug34_solve_rate'] = float(0)  # bug34解决率
            else:
                bug['bug34_solve_rate'] = float(sql_return_result_tuple[0][3]) * 100  # bug34解决率

            # bug['easy_bug_rate'] = str((float(sql_return_result_tuple[0][3]) * 100)) + '%'  # 易bug比率,str echarts无法显示

            # 后面是项目相关的 ，有几个项目循环几次
            for developer in developer_tuple:
                # 当前索引
                # print(f'当前developer=={str(developer)}')
                index = developer_tuple.index(developer)
                # print(f'当前索引=={index}')
                # print(f'第{index}次循环开始================================================')

                #   str1808[1:len(str1808)-2] 截取字符串 中developer名字--》'1808'
                #   str1808[2:len(str1808)-3] 截取字符串 中developer名字--》1808 (去掉''格式的)
                bug['developer' + str(index)] = str(developer)[2:len(str(developer)) - 3]  # 项目名称并不是从sql语句中读出来的，developer sql语句中读出
                # bug解决率有可能出现none的情况
                if sql_return_result_tuple[0][4 + index*2] is None:
                    # bug['easy_bug_rate_developer' + str(index)] = str((float(0) * 100)) + '%'  # bug12解决率
                    bug['bug12_solve_rate_developer' + str(index)] = float(0) * 100  # bug及时率
                else:
                    bug['bug12_solve_rate_developer' + str(index)] = float(sql_return_result_tuple[0][4 + index*2]) * 100  # bug12解决率

                if sql_return_result_tuple[0][4 + index*2 + 1] is None:
                    # bug['easy_bug_rate_developer' + str(index)] = str((float(0) * 100)) + '%'  # bug12解决率
                    bug['bug34_solve_rate_developer' + str(index)] = float(0) * 100  # bug及时率
                else:
                    bug['bug34_solve_rate_developer' + str(index)] = float(sql_return_result_tuple[0][4 + index*2 + 1]) * 100  # bug12解决率

                # print(f'developer{index}=', bug['developer' + str(index)])  #
                # print(f'add_developer{index}=', bug['add_developer' + str(index)])
                # print(f'close_developer{index} ==', bug['close_developer' + str(index)])
                # print(f'regression_developer{index}  ===', bug['regression_developer' + str(index)])
                # print(f'delay_developer{index}  ===', bug['delay_developer' + str(index)])
                #
                # print(f'第{index}次循环结束================================================')

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
    print('<admin.py> 搜索bug及时率 type(data)== ', type(data))
    print('<admin.py> 搜索bug及时率 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('<buglist> get_bugsolverate_table_fordrawmap_withdeveloper_orderby_date,返回结果==jsonStr=====', json_str)

    print('=================================获取所有 开发维度,一定时间颗粒度,bug解决率 的数据 end ===================================')
    # 这些只是从数据库中，查出来的每天的数据，前端需要求和处理
    return json_str