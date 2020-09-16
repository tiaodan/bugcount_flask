import xlrd
import pymysql
import json
#  引入python中的traceback模块，跟踪错误
import traceback
from py import utils

# 数据库配置
"""
db_host = 'localhost'
db_user = 'root'
db_passwd = 'sunkaisens'
db_dbname = 'bugcount'
"""
print('<dbutil.py>获取。。。。。。。。。。。。。。。。config文件 start')
db_config_dict = utils.get_dbargs_from_config_byabspath()
# db_config_dict = utils.get_dbargs_from_config()

db_host = db_config_dict['db_host']
db_user = db_config_dict['db_user']
db_passwd = db_config_dict['db_passwd']
db_dbname = db_config_dict['db_dbname']
print('<dbutil.py>获取。。。。。。。。。。。。。。。。config文件 end ')

# 数据库操作
class DB():
    def __init__(self, host='localhost', port=3306, db='', user='root', passwd='sunkaisens', charset='utf8'):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()


# 定义数据库操作
# 参数 ip  用户名 密码 数据库名,必须要传1个参数
def withDB(sql1, *sqlN):
    #    with DB(host='localhost', user='root', passwd='123456', db='bugcount') as db:
    with DB(host=db_host, user=db_user, passwd=db_passwd, db=db_dbname) as db:
        # db.execute('show databases')
        # 默认执行第一条语句
        db.execute(sql1)
        # 执行结果
        print(db)
        for i in db:
            print(i)

        # 查询方法参数个数，根据参数个数执行语句
        print("sql1==", sql1)
        print("sqlN==", sqlN)

        fun_args_nums = len(sqlN)
        print("方法参数个数有： %s " % len(sqlN))
        print("不确定参数，第一个数为====", sqlN[0])
        if fun_args_nums == 1:
            # 执行第二条语句
            db.execute(sqlN[0])
            # 执行结果
            print(db)
            for i in db:
                print(i)
        db.close()


# 测试链接，打印版本

def db_test():
    # 打开数据库连接
    db = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print("Database version : %s " % data)

    # 关闭数据库连接
    cursor.close()
    db.close()


# 打开数据库
# 1. sql 2. 参数后面的匹配变量
def execute_db_onesql(sql, *args):
    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数
    sql_return_result_tuple = ()  # 执行sql会返回tuple

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    print(f'sql语句为==', sql)
    print("*args====", args)
    print('参数args类型=={args}', type(args))

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 执行sql语句
        cursor.execute(sql, args)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()
        print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        # 转化下查询结果为{},{},{}这种格式
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'sql语句执行成功'
        return_list = [code, msg, count, sql_return_result_tuple]
        print(f'《返回结果》 return_list===={return_list}')
        print('拼接返回给 《调用者》 的 数据类型====', type(return_list))


    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
        # 拼接返回数据,返回列表
        return_list = [code, msg, count, sql_return_result_tuple]
        print('sql异常 执行sql 返回的数据====', return_list)

    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    return return_list

# 通过excel导入mysql
def import_mysql_by_excel():
    # json数据
    data = {}
    buglist = []

    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据所在的工作簿，以及选择存有数据的工作表
    # book = xlrd.open_workbook("../excel_upload/buglist.xls")
    book = xlrd.open_workbook("./excel_upload/template.xlsx")
    sheet = book.sheet_by_name("Sheet1")
    # 建立一个MySQL连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 获得游标
    cur = conn.cursor()
    # 创建插入SQL语句
    # query = 'insert into bugcount.buglist (name,sex,minzu,danwei_zhiwu,phone_number,home_number) values (%s, %s, %s, %s, %s, %s)'
    # query = 'INSERT INTO `buglist` VALUES ('2', '2020-01-10', '1808', 'icss', 'icss_disp_20200108', '调度台无法强插', '3', '2', '2', '1', '0', null, null, null, null, '李东东', null, null, null, null, null, null, null, null, null, null);'
    query = 'insert into bugcount.buglist (bugid, bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark, second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark, third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark) ' \
            'values (null, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s) ' \
            'on duplicate key update bug_submit_date=%s,project=%s,software=%s,test_version=%s,severity_level=%s,priority=%s,bug_difficulty=%s,bug_status=%s,bug_close_date=%s,close_version=%s,cause_analysis=%s,bug_img=%s,intermediate_situation=%s,developer=%s,remark=%s' \
            ',first_bug_regression_date=%s,first_bug_regression_status=%s,first_bug_regression_remark=%s,second_bug_regression_date=%s,second_bug_regression_status=%s,second_bug_regression_remark=%s,third_bug_regression_date=%s,third_bug_regression_status=%s,third_bug_regression_remark=%s'
    #dao bug_close_date

    print(query)
    #values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)'
    # query = 'insert into bugcount.buglist (bug_submit_date, project, software, test_version) values (%s, %s, %s, %s)'

    # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行

    for r in range(1, sheet.nrows):
        print('Nlie nrows==', sheet.nrows)
        print('curent r ==', r)
        n = 1
        print('shel.cell', sheet.cell(r, n))

        # bug_submit_date_noformat = datetime.datetime.strptime(str(sheet.cell(r, 0).value), '%Y-%m-%d').time()
        # time.strftime("%Y-%m-%d %H:%M:%S", sheet.cell(r, 0).value)
        bug_submit_date = sheet.cell(r, 0).value
        project = sheet.cell(r, 1).value
        software = sheet.cell(r, 2).value
        test_version = sheet.cell(r, 3).value
        bug_description = sheet.cell(r, 4).value
        severity_level = sheet.cell(r, 5).value
        priority = sheet.cell(r, 6).value
        bug_difficulty = sheet.cell(r, 7).value
        bug_status = sheet.cell(r, 8).value
        bug_close_date = sheet.cell(r, 9).value
        close_version = sheet.cell(r, 10).value
        cause_analysis = sheet.cell(r, 11).value
        bug_img = sheet.cell(r, 12).value
        intermediate_situation = sheet.cell(r, 12).value
        developer = sheet.cell(r, 14).value
        remark = sheet.cell(r, 15).value
        first_bug_regression_date = sheet.cell(r, 16).value
        print('cell_type 17= ', type(sheet.cell(r, 17).ctype))

        first_bug_regression_status = sheet.cell(r, 17).value
        first_bug_regression_remark = sheet.cell(r, 18).value
        second_bug_regression_date = sheet.cell(r, 19).value
        second_bug_regression_status = sheet.cell(r, 20).value
        second_bug_regression_remark = sheet.cell(r, 21).value
        third_bug_regression_date = sheet.cell(r, 22).value
        third_bug_regression_status = sheet.cell(r, 23).value
        third_bug_regression_remark = sheet.cell(r, 24).value
        n += 1

        # values = (name, sex, minzu, danwei_zhiwu, phone_number, home_number) 第一行插入所需的变量（25个，除去bugid）;第二行数据相同更新参数（24个-出去bugid 喝bug_description）
        values = (bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark, second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark, third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark,
                  bug_submit_date, project, software, test_version, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark, second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark, third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark)

        # values = (bug_submit_date, project, software, test_version)
        print('valuse=', values)

        # 执行sql语句
        cur.execute(query, values)
        code = 200
        msg = '导入数据成功'
    conn.commit()
    cur.close()
    conn.close()
    columns = str(sheet.ncols)
    rows = str(sheet.nrows)
    print("导入 " + columns + " 列 " + rows + " 行数据到MySQL数据库!")

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str

# 获取用户数据
def getUserList():
    # 打开数据库连接

    print(f'数据库配置{db_host}，{db_user}, {db_passwd}, {db_dbname}')
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname,)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    sql = 'select * from bugcount.user'
    cursor.execute(sql)
    print('共有', cursor.rowcount, '条数据')

    users = []
    data = {}
    results = cursor.fetchall()
    for r in results:
        print(r[0], end=' ')
        print(r[1], end=' ')
        print(r[2], end=' ')
        print("---")
        person = {}
        person['id'] = r[0]
        person['name'] = r[1]
        person['pass'] = r[2]
        users.append(person)
    cursor.close()
    conn.close()
    data['code'] = 200
    data['msg'] = '成功'
    # data['msg'] = 'suesss'

    data['users'] = users
    json_str = json.dumps(data)
    print(json_str)

    return json_str



# 1. sql 2. 参数后面的匹配变量
def register(*args):

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
    print("*args====", args)
    print('参数args类型=={args}', type(args))

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 执行sql语句 角色默认是普通用户 -2
        sql = 'insert into bugcount.user (userid, username, password, user_remark, user_email, user_level, create_time, session, roleId)values(null, %s, %s, null, null, null, null, null, 2)'
        cursor.execute(sql, args)
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
            print('=============进入循环')
            print('=============进入循环r0', r[0])
            print('=============进入循环r1', r[1])
            print('=============进入循环r2', r[2])
            print('=============进入循环r3', r[3])
            print('=============进入循环r4', r[4])
            print('=============进入循环r5', r[5])
            print('=============进入循环r6', str(r[6]))
            print('=============进入循环r7', r[7])

            person = dict()
            person['userid'] = r[0]
            person['username'] = r[1]
            person['password'] = r[2]
            person['user_remark'] = r[3]
            person['user_email'] = r[4]
            person['user_level'] = r[5]
            person['create_time'] = str(r[6])
            person['session'] = r[7]
            # print('==============循环person==', person)

            users.append(person)
            print('????dbutil 转换完的【{}】格式数据users==', users)

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'sql语句执行成功'
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


# login 登录
def login(*args):

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
        sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user where username = %s and password = %s'
        print(f'sql语句为==', sql)
        print("*args====", args)
        print('参数args类型=={args}', type(args))

        # 执行sql语句
        cursor.execute(sql, args)
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
            print('=============进入循环')
            print('=============进入循环r0', r[0])
            print('=============进入循环r1', r[1])
            print('=============进入循环r2', r[2])
            print('=============进入循环r3', r[3])
            print('=============进入循环r4', r[4])
            print('=============进入循环r5', r[5])
            print('=============进入循环r6', str(r[6]))
            print('=============进入循环r7', r[7])

            person = dict()
            person['userid'] = r[0]
            person['username'] = r[1]
            person['password'] = r[2]
            person['user_remark'] = r[3]
            person['user_email'] = r[4]
            person['user_level'] = r[5]
            person['create_time'] = str(r[6])
            person['session'] = r[7]
            # print('==============循环person==', person)

            users.append(person)
            print('????dbutil 转换完的【{}】格式数据users==', users)

        # 拼接返回数据,返回列表
        count = len(sql_return_result_tuple)  # sql语句结果个数

        # 判断是否 能登录
        if count > 0:
            code = 200  # 成功
            msg = '有此用户，可正常登录'

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

# 检查用户名是否 数据库是否被占用 True:code=200 False: code=500
def check_username_is_registered(username):

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
        # 执行sql语句
        sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user where username=%s'
        print(f'sql语句为==', sql)
        print("*args====", username)
        print('参数args类型=={args}', type(username))

        cursor.execute(sql, username)
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
            print('=============进入循环')
            person = {}
            person['userid'] = r[0]
            person['username'] = r[1]
            person['password'] = r[2]
            person['user_remark'] = r[3]
            person['user_email'] = r[4]
            person['user_level'] = r[5]
            person['create_time'] = str(r[6])
            person['session'] = r[7]

            users.append(person)
            print('????dbutil 转换完的【{}】格式数据users==', users)

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'sql语句执行成功'
        print('?????????????????????josn sql_return_result_tuple type = ', type(len(sql_return_result_tuple)))
        count = len(sql_return_result_tuple)  # sql语句结果个数
    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    print('?????????????????????josn count type = ', type(data['count']))
    data['json_data'] = users
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str

