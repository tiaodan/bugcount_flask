"""
管理员相关业务：
增删改查


"""
import xlrd
import pymysql
import json
#  引入python中的traceback模块，跟踪错误
import traceback
from py import utils



# 获取数据库配置
print('获取。。。。。。。。。。。。。。。。config文件')
db_config_dict = utils.get_dbargs_from_config()

db_host = db_config_dict['db_host']
db_user = db_config_dict['db_user']
db_passwd = db_config_dict['db_passwd']
db_dbname = db_config_dict['db_dbname']

print('获取。。。。。。。。。。。。。。。。config文件 end ')



# 查询所有用户
# page = 当前页码，limit=当前页码显示个数
def search_users(page, limit):

    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    #json数据
    data = {}
    users = []

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
        # sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user limit 0,40'
        sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user limit %s,%s'
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

        # 转化下查询结果为{},{},{}这种格式======================
        print('????????result=', sql_return_result_tuple)
        print('????????????????????type = ', type(sql_return_result_tuple))


        for r in sql_return_result_tuple:
            """
            
            print('=============进入循环')
            print('=============进入循环r0', r[0])
            print('=============进入循环r1', r[1])
            print('=============进入循环r2', r[2])
            print('=============进入循环r3', r[3])
            print('=============进入循环r4', r[4])
            print('=============进入循环r5', r[5])
            print('=============进入循环r6', r[6])
            print('=============进入循环r7', r[7])
            """
            person = dict()
            person['userid'] = r[0]
            print('=============================r=', r)
            print('=============================userid=',  person['userid'])
            person['username'] = r[1]
            person['password'] = r[2]
            person['user_remark'] = r[3]
            person['user_email'] = r[4]
            person['user_level'] = r[5]
            person['create_time'] = str(r[6])  # 转成str，否则会报TypeError: Object of type datetime is not JSON serializable
            person['session'] = r[7]
            print('==============循环person==', person)

            users.append(person)
        print('????dbutil 转换完的【{}】格式数据users==', users)

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
    data['data'] = users
    # 转化下查询结果为{},{},{}这种格式======================
    print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


def add_user(*args):
    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    # json数据
    data = {}
    users = []

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

        # sql = 'selectselect userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user limit %s,%s'
        # 默认userid 是null 就按顺序加入mysql
        sql = 'insert into bugcount.user (userid, username, password, user_remark, user_email, user_level, create_time, session) value (null, %s, %s, %s, %s, %s, %s, %s)'
        print(f'sql语句为==', sql)
        print('sql语句参数 *args==== }', args)
        print('sql语句参数 *args type==== }', type(args))

        # username, password, user_remark, user_email, user_level, create_time, session
        # print('sql语句参数args类型=={args}', type(args))

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        # 判断传入的日期参数 ，如果是空的话，不给sql语句传值就可以了，但是args是tuple类型，不支持删除--》转成list，将time替换成None
        if args[5] == '':  # create_time是空
            args_list = list(args)
            print('将crete_time复制None')
            args_list[5] = None
            args = tuple(args_list)

        cursor.execute(sql, args)
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
            """

            print('=============进入循环')
            print('=============进入循环r0', r[0])
            print('=============进入循环r1', r[1])
            print('=============进入循环r2', r[2])
            print('=============进入循环r3', r[3])
            print('=============进入循环r4', r[4])
            print('=============进入循环r5', r[5])
            print('=============进入循环r6', r[6])
            print('=============进入循环r7', r[7])
            """
            person = dict()
            person['userid'] = r[0]
            person['username'] = r[1]
            person['password'] = r[2]
            person['user_remark'] = r[3]
            person['user_email'] = r[4]
            person['user_level'] = r[5]
            person['create_time'] = str(r[6])  # 转成str，否则会报TypeError: Object of type datetime is not JSON serializable
            print('person(create_time)===', person['create_time'])
            if person['create_time'] == '':
                print('person(create_time)===空')
                person['create_time'] = None
            person['session'] = r[7]
            print('==============循环person==', person)

            users.append(person)
            print('????dbutil 转换完的【{}】格式数据users==', users)

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        # if count > 0:
        code = 200  # 成功
        msg = 'add user语句执行成功'

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
    data['data'] = users
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str

def del_user(userid):

    # json数据
    data = {}
    users = []

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

        sql = 'delete from  bugcount.user where userid = %s'
        print(f'sql语句为==', sql)
        print('sql语句参数 *args==== }', userid)
        print('sql语句参数 *args type==== }', type(userid))

        cursor.execute(sql, userid)
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
        msg = 'deluser语句执行成功'
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
    data['data'] = users
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str

# 编辑用户
def edit_user(*args):

    # json数据
    data = {}
    users = []

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

        sql = 'update bugcount.user set username=%s, password=%s, user_remark=%s, user_email=%s, user_level=%s, create_time=%s, session=%s where userid=%s'
        # sql = 'update bugcount.user set user_remark=%s where userid=%s' #测试用的语句
        # sql = 'update bugcount.user set username=%s, password=%s, user_remark=%s, user_email=%s, user_level=%s, create_time=%s, session=%s where userid=%s' #测试用的语句
        print(f'sql语句为==', sql)
        print('sql语句参数 *args==== }', args)
        print('sql语句参数 *args type==== }', type(args))
        print(f'完整的sqlw为 ：update bugcount.user set username={args[1]}, password={args[2]}, user_remark={args[3]}, user_email={args[4]}, user_level={args[5]}, create_time={args[6]}, session={args[7]} where userid={args[0]}')

        # userid, username, password, user_remark, user_email, user_level, create_time, session
        # print('sql语句参数args类型=={args}', type(args))

        # cursor.execute那句 sql的所有参数，应该都写到中括号里面，以逗号分割  [pageBegin,IntPageSize])
        # 判断传入的日期参数 ，如果是空的话，不给sql语句传值就可以了，但是args是tuple类型，不支持删除--》转成list，将time替换成None
        if args[6] == '' or args[6] == 'None':
            args_list = list(args)
            print('将crete_time复制None')
            args_list[6] = None
            args = tuple(args_list)

        # 多参数，execute要传2个参数，sql 和args分解出来的
        print('type(args)===================================', type(args))
        # cursor.execute(sql, args)  # 偶尔不好用
        args_test = [args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[0]]  # 测试用
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

            person = dict()
            person['userid'] = r[0]
            person['username'] = r[1]
            person['password'] = r[2]
            person['user_remark'] = r[3]
            person['user_email'] = r[4]
            person['user_level'] = r[5]
            person['create_time'] = str(r[6])  # 转成str，否则会报TypeError: Object of type datetime is not JSON serializable
            print('person(create_time)===', person['create_time'])
            """
            if person['create_time'] == '':
                print('person(create_time)===空')
                person['create_time'] = None
            """
            person['session'] = r[7]
            print('==============循环person==', person)

            users.append(person)
            print('????dbutil 转换完的【{}】格式数据users==', users)

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
    data['data'] = users
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str