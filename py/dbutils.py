import xlrd
import xlwt
import pymysql
import json
#  引入python中的traceback模块，跟踪错误
import traceback
import os
import xlsxwriter
from py import utils
from collections import Counter
from datetime import datetime

# 数据库配置
"""
db_host = 'localhost'
db_user = 'root'
db_passwd = 'sunkaisens'
db_dbname = 'bugcount'
"""
print('<dbutil.py>获取。。。。。。。。。。。。。。。。config文件 start')
db_config_dict = utils.get_dbargs_from_config_byabspath()
db_host = db_config_dict['db_host']
db_user = db_config_dict['db_user']
db_passwd = db_config_dict['db_passwd']
db_dbname = db_config_dict['db_dbname']
print('<dbutil.py>获取。。。。。。。。。。。。。。。。config文件 end ')

# 初始化变量
currentpath = os.path.abspath(__file__)
print('当前路径', currentpath)
rootdir = os.path.abspath(os.path.dirname(currentpath) + os.path.sep + '..')  # 当前路径上一层
print('根目录==', rootdir)

# 定义一个字典，用于英文表头--》中文表头
tableheaddict = {
	"bug_submit_date": "提交日期",
	"project": "项目",
	"software": "软件类",
	"test_version": "测试版本",
	"bug_description": "描述",
	"severity_level": "严重等级",
	"priority": "优先级",
	"bug_difficulty": "难度",
	"bug_status": "关闭情况",
	"bug_close_date": "关闭日期",
	"close_version": "关闭版本",
	"cause_analysis": "原因分析",
	"bug_img": "问题图片",
	"intermediate_situation": "中间情况",
	"developer": "开发者",
	"remark": "备注",
	"regression_times": "回归次数",
	"reopen_times": "重开次数",
	"submitterindex": "提交者索引",
	None: "" # 导出的表格不能出现None,因为再次导入，日期格式如果是None会报错.可以直接使用aa[None] 调用
}



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
def execute_db_onesql_nouse(sql, *args):
    # 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数
    sql_return_result_tuple = ()  # 执行sql会返回tuple

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # print(f'sql语句为==', sql)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

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
    msg = '导入失败'
    count = 0  # sql语句执行结果个数
    isrepeat = 0  # 1有，0没有
    repeatlist = []  # 提交者索引 重复内容

    # 打开数据所在的工作簿，以及选择存有数据的工作表
    # book = xlrd.open_workbook("../excel_upload/buglist.xls")
    tablehead = ['提交日期', '项目', '软件类', '测试版本', '描述',
                 '严重等级', '优先级', '难度', '关闭情况', '关闭日期',
                 '关闭版本', '原因分析', '问题图片', '中间情况', '开发者',
                 '备注', '回归次数', '重开次数', '提交者索引']
    book = xlrd.open_workbook("./excel_upload/template.xlsx")

    # 1. 检测xecel表格内容是否符合标准
    is_exceldata_ok_jsonstr = utils.checkexcel_data("./excel_upload/template.xlsx", tablehead)
    is_exceldata_ok_jsonobj = json.loads(is_exceldata_ok_jsonstr)
    check_excel_code = is_exceldata_ok_jsonobj['code']
    if check_excel_code == 200:

        # 建立一个MySQL连接
        conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
        # 获得游标
        cur = conn.cursor()

        # 1. 读取每一个sheet名称,并将可见的sheet组成一个list
        sheetnames = book.sheet_names()
        showsheet_names = list()
        hidesheet_names = list()
        for sheetname in sheetnames:
            sheet = book.sheet_by_name(sheetname)
            if sheet.visibility == 0:  # 可见
                showsheet_names.append(sheet.name)
            else:  # ==1 不可见
                hidesheet_names.append(sheet.name)
        print("??????????????显示sheet==", showsheet_names)
        print("??????????????隐藏sheet==", hidesheet_names)
        print("??????sheets===", sheetnames)

        # 2. 循环写入数据
        for showsheet_name in showsheet_names:
            print('????当前sheet==', showsheet_name)
            sheet = book.sheet_by_name(showsheet_name)
            # sheet = book.sheet_by_name("Sheet1")

            # 创建插入SQL语句 带第一次回归、第二次回归、第三次回归相关列表的sql
            # query = 'insert into bugcount.buglist (name,sex,minzu,danwei_zhiwu,phone_number,home_number) values (%s, %s, %s, %s, %s, %s)'
            # query = 'INSERT INTO `buglist` VALUES ('2', '2020-01-10', '1808', 'icss', 'icss_disp_20200108', '调度台无法强插', '3', '2', '2', '1', '0', null, null, null, null, '李东东', null, null, null, null, null, null, null, null, null, null);'
            # sql = 'insert into bugcount.buglist (bugid, bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark, second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark, third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark) ' \
            #         'values (null, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s) ' \
            #         'on duplicate key update bug_submit_date=%s,project=%s,software=%s,test_version=%s,severity_level=%s,priority=%s,bug_difficulty=%s,bug_status=%s,bug_close_date=%s,close_version=%s,cause_analysis=%s,bug_img=%s,intermediate_situation=%s,developer=%s,remark=%s' \
            #         ',first_bug_regression_date=%s,first_bug_regression_status=%s,first_bug_regression_remark=%s,second_bug_regression_date=%s,second_bug_regression_status=%s,second_bug_regression_remark=%s,third_bug_regression_date=%s,third_bug_regression_status=%s,third_bug_regression_remark=%s'

            sql = 'insert into bugcount.buglist (bugid, bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, regression_times, reopen_times, submitterindex) ' \
                  'values (null, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
                  'on duplicate key update bug_submit_date=%s,project=%s,software=%s,test_version=%s,bug_description=%s,severity_level=%s,priority=%s,bug_difficulty=%s,bug_status=%s,bug_close_date=%s,close_version=%s,cause_analysis=%s,bug_img=%s,intermediate_situation=%s,developer=%s,remark=%s,regression_times=%s,reopen_times=%s'

            print('sql==', sql)

            # 执行前先判断索引列（submitterindex）是否有重复的，提示用户,重复的行是submitterindex_col_list[n] +1
            submitterindex_col_list = []
            for r in range(1, sheet.nrows):
                submitterindex = sheet.cell(r, 18).value
                submitterindex_col_list.append(submitterindex)
            for k, v in Counter(submitterindex_col_list).items():
                if v > 1:
                    isrepeat = 1  # 有重复选项
                    msg = '上传的execel表索引有重复，请检查submitterindex列'
                    print('重复的元素', k)
                    repeatlist.append(k)

            if isrepeat != 1:  # 没有重复项
                # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
                for r in range(1, sheet.nrows):
                    # print('Nlie nrows==', sheet.nrows)
                    # print('curent r ==', r)
                    n = 1
                    # print('shel.cell', sheet.cell(r, n))

                    # bug_submit_date_noformat = datetime.strptime(str(sheet.cell(r, 0).value), '%Y-%m-%d').time()
                    # time.strftime("%Y-%m-%d %H:%M:%S", sheet.cell(r, 0).value)
                    bug_submit_date = sheet.cell(r, 0).value
                    # print('!!!!!!!!!!!!!!!!!!!!bug_submit_date', sheet.cell(r, 0).value)
                    if bug_submit_date is None or bug_submit_date == '':
                        # bug_submit_date = "1888-01-01"
                        bug_submit_date = None
                    elif type(bug_submit_date) == float:
                        # 类型为时间戳
                        bug_submit_date = xlrd.xldate.xldate_as_datetime(sheet.cell(r, 0).value, 0).strftime("%Y-%#m-%#d")  # 应该传一个时间数值
                        # print("转换时间戳完成后", bug_submit_date)
                    elif type(bug_submit_date) == str:
                        # 上传时为xxxx/xx/xx这种格式，转化成  xxxx-zz-zz
                        bug_submit_date = bug_submit_date.replace("/", "-")
                        # bug_submit_date = datetime.strftime(datetime.strptime(bug_submit_date, "%Y/%m/%d"), "%Y-%#m-%#d")
                    # print('!!!!!!!!!!!!!!!!!!!!bug_submit_date 转换后type', type(bug_submit_date))
                    # print('!!!!!!!!!!!!!!!!!!!!bug_submit_date 转换后', bug_submit_date)
                    # 因为excel里面是2020/01/10这种格式的，所以需要转化

                    project = sheet.cell(r, 1).value
                    software = sheet.cell(r, 2).value
                    test_version = sheet.cell(r, 3).value
                    bug_description = sheet.cell(r, 4).value
                    severity_level = sheet.cell(r, 5).value  # 严重等级
                    if severity_level is None or severity_level == '':
                        severity_level = None
                    priority = sheet.cell(r, 6).value  # 优先级
                    if priority is None or priority == '':
                        priority = None
                    bug_difficulty = sheet.cell(r, 7).value
                    if bug_difficulty is None or bug_difficulty == '':
                        bug_difficulty = None
                    bug_status = sheet.cell(r, 8).value  # float
                    # 将用户导入的“关闭情况” --》转成数字
                    # 1 处理(handle)，2 关闭(close)，3 回归(regression)，4 延迟(delay)， 5 重开(reopen) 0 未知（可能用户上传时bug_status字段不对）//excel上传导入时，填写中文、英文均可
                    if bug_status == "处理" or bug_status == "handle":
                        bug_status = 1
                    elif bug_status == "关闭" or bug_status == "close":
                        bug_status = 2
                    elif bug_status == "回归" or bug_status == "regression":
                        bug_status = 3
                    elif bug_status == "延迟" or bug_status == "delay":
                        bug_status = 4
                    elif bug_status == "重开" or bug_status == "reopen":
                        bug_status = 5
                    else:
                        bug_status = 0  # 未知（可能用户上传时bug_status字段不对）

                    bug_close_date = sheet.cell(r, 9).value
                    # print('!!!!!!!!!!!!!!!!!!!!bug_close_dateexcel日期类型 前', bug_close_date)
                    if bug_close_date is None or bug_close_date == '':
                        bug_close_date = None
                    elif type(bug_close_date) == float:
                        bug_close_date = xlrd.xldate.xldate_as_datetime(sheet.cell(r, 9).value, 0).strftime("%Y-%#m-%#d")
                        # print("转换时间戳完成后bug_close_date", bug_submit_date)
                    elif type(bug_close_date) == str:
                        # 类型为xxxx/xx/xx这种格式，转化成  xxx    x-zz-zz
                        bug_close_date = bug_close_date.replace("/", "-")
                        # bug_close_date = datetime.strftime(datetime.strptime(bug_close_date, "%Y/%m/%d"), "%Y-%#m-%#d")
                    # print('!!!!!!!!!!!!!!!!!!!!bug_close_dateexcel日期类型 后', type(bug_close_date))
                    # print('!!!!!!!!!!!!!!!!!!!!bug_close_dateexcel日期 后', bug_close_date)

                    close_version = sheet.cell(r, 10).value
                    cause_analysis = sheet.cell(r, 11).value
                    bug_img = sheet.cell(r, 12).value
                    intermediate_situation = sheet.cell(r, 12).value
                    developer = sheet.cell(r, 14).value
                    remark = sheet.cell(r, 15).value
                    regression_times = sheet.cell(r, 16).value
                    # print("regression_times==============================", regression_times)
                    if regression_times is None or regression_times == '':
                        regression_times = None
                    reopen_times = sheet.cell(r, 17).value
                    # print("reopen_times==============================", reopen_times)
                    if reopen_times is None or reopen_times == '':
                        reopen_times = None
                    submitterindex = sheet.cell(r, 18).value
                    # print('-------查到的索引==', submitterindex)
                    n += 1

                    # values = (name, sex, minzu, danwei_zhiwu, phone_number, home_number) 第一行插入所需的变量（25个，除去bugid）;第二行数据相同更新参数（24个-出去bugid 喝bug_description）
                    values = (
                    bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty,
                    bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer,
                    remark, regression_times, reopen_times, submitterindex,
                    bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty,
                    bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer,
                    remark, regression_times, reopen_times)
                    # print("!!!!!!!!!!!!!!导入values", values)

                    # values = (bug_submit_date, project, software, test_version)
                    # print('import_mysql_by_excel（）方法 valuse=', values)
                    # 执行sql语句
                    cur.execute(sql, values)
                    code = 200
                    msg = '导入数据成功'
                conn.commit()
                columns = str(sheet.ncols)
                rows = str(sheet.nrows)
                print("导入 " + columns + " 列 " + rows + " 行数据到MySQL数据库!")

        cur.close()
        conn.close()

        #  返回json格式的数据
        data['code'] = code
        data['msg'] = msg
        data['count'] = count
        data['data'] = buglist
        data['isrepeat'] = isrepeat
        data['repeatlist'] = repeatlist
        # 转化下查询结果为{},{},{}这种格式======================
        json_str = json.dumps(data, ensure_ascii=False)
        print('dbutil==jsonStr=====', json_str)
        return json_str

    # 加上是否重复
    is_exceldata_ok_jsonobj['isrepeat'] = 0  # 1有，0没有
    is_exceldata_ok_jsonobj['repeatlist'] = []  # 提交者索引 重复内容
    is_exceldata_ok_jsonstr = json.dumps(is_exceldata_ok_jsonobj)
    return is_exceldata_ok_jsonstr


# 获取用户数据
def getUserList():
    # 打开数据库连接

    print(f'数据库配置{db_host}，{db_user}, {db_passwd}, {db_dbname}')
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname, )

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
    # json数据
    data = {}
    users = []

    # 默认定义数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

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

        # 转换查询结果为[{},{},{}]这种格式的
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
        sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user where username = %s and password = %s'
        # print(f'sql语句为==', sql)
        # print("*args====", args)
        # print('参数args类型=={args}', type(args))

        # 执行sql语句
        cursor.execute(sql, args)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        # 转化下查询结果为{},{},{}这种格式======================
        # print('????????result=', sql_return_result_tuple)
        # print('????????????????????type = ', type(sql_return_result_tuple))

        for r in sql_return_result_tuple:
            # print('=============进入循环')
            # print('=============进入循环r0', r[0])
            # print('=============进入循环r1', r[1])
            # print('=============进入循环r2', r[2])
            # print('=============进入循环r3', r[3])
            # print('=============进入循环r4', r[4])
            # print('=============进入循环r5', r[5])
            # print('=============进入循环r6', str(r[6]))
            # print('=============进入循环r7', r[7])

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
        # 执行sql语句
        sql = 'select userid,username,password,user_remark,user_email,user_level,create_time,session from bugcount.user where username=%s'
        # print(f'sql语句为==', sql)
        # print("*args====", username)
        # print('参数args类型=={args}', type(username))

        cursor.execute(sql, username)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))
        print("sql语句执行成功")

        # 转化下查询结果为{},{},{}这种格式======================
        print('????????result=', sql_return_result_tuple)
        print('????????????????????type = ', type(sql_return_result_tuple))
        for r in sql_return_result_tuple:
            # print('=============进入循环')
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
        # print('?????????????????????josn sql_return_result_tuple type = ', type(len(sql_return_result_tuple)))
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
    data['json_data'] = users
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


"""
功能：导出数据库表中所有数据到 excel数据
"""


def export(tablename, outputpath):
    # json数据
    data = {}
    buglist = []
    code = 500  # 默认失败
    msg = '导出失败'
    count = 0  # sql语句执行结果个数

    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname, charset='utf8')
    cursor = conn.cursor()
    sql = 'select bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, regression_times, reopen_times, submitterindex from ' + tablename
    print('<dbutils> 导出数据 sql ==', sql)

    count = cursor.execute(sql)
    print(count)
    # 重置游标的位置
    cursor.scroll(0, mode='absolute')
    # 搜取所有结果
    results = cursor.fetchall()

    # 获取MYSQL里面的数据字段名称
    fields = cursor.description
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    # sheet = workbook.add_sheet('table_'+table_name, cell_overwrite_ok=True)
    sheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)  # 写入sheet1

    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(results) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row - 1][col])
    # 写文件，如果目录文件不存在，则创建
    workbook.save(outputpath)

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    data['isrepeat'] = isrepeat
    data['repeatlist'] = repeatlist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 功能：执行一条sql语句
# 1. sql 2. 参数后面的匹配变量
def execute_onesql(sql, *args):
    # 初始化数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数
    sql_return_result_tuple = ()  # 执行sql会返回tuple

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # print('sql语句为==', sql)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

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
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))  # tuple
        print("sql语句执行成功")

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'sql语句执行成功'
    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
        return 0  # 异常返回数字0
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    # print('返回数据如下：')
    # print(sql_return_result_tuple)
    return sql_return_result_tuple


# 功能：执行一条sql语句,并返回表头数据
# 1. sql 2. 参数后面的匹配变量
def execute_onesql_returnth(sql, *args):
    # 初始化数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数
    sql_return_result_tuple = ()  # 执行sql会返回tuple

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # print('sql语句为==', sql)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        # 执行sql语句
        cursor.execute(sql, args)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.description
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))  # tuple
        print("sql语句执行成功")

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'sql语句执行成功'
    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
        return 0  # 异常返回数字0
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    # print('返回数据如下：')
    # print(sql_return_result_tuple)
    return sql_return_result_tuple


# 功能：执行一条sql语句,返回json数据
# 1. sql 2. 参数后面的匹配变量
def execute_onesql_returnjson(sql, *args):
    # 初始化数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数
    data = {}
    jsondatas = []  # data:{jsondatas}

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # print('sql语句为==', sql)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

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
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))  # tuple
        print("sql语句执行成功")

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'sql语句执行成功'
        count = len(sql_return_result_tuple)
    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
        return 0  # 异常返回数字0
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    # 5.返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = jsondatas
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('<dbutil.py> (execute_onesql_returnjson) 返回jsonStr=====', json_str)
    return json_str


# 功能：执行一条sql语句,返回json数据.里面sqlresultcode =
# 1. sql 2. 参数后面的匹配变量
def execute_onesql_returnjson_privilege(sql, *args):
    # 初始化数据
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数
    data = {}
    jsondatas = []  # data:{jsondatas}
    privilege_int = 0

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # print('sql语句为==', sql)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

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
        print("获取权限，执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        print("获取权限执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        print("获取权限执行语句返回结果(类型)==", type(sql_return_result_tuple))  # tuple
        print("获取权限sql语句执行成功")

        # 拼接返回数据,返回列表
        code = 200  # 成功
        msg = 'sql语句执行成功'
        count = len(sql_return_result_tuple)
        privilege_int = sql_return_result_tuple[0]
    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
        return 0  # 异常返回数字0
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    # 5.返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = jsondatas
    data['privilege_int'] = privilege_int
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('<dbutil.py> (execute_onesql_returnjson) 返回jsonStr=====', json_str)
    return json_str


# 功能：执行一条sql语句,返回int数据
# 1. sql 2. 参数后面的匹配变量
def execute_onesql_returnint(sql, *args):
    # 初始化数据
    result_int = 0  # sql语句执行结果

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # print('sql语句为==', sql)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

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
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))  # tuple
        print("sql语句执行成功")

        # 拼接返回数据,返回列表
        result_int = sql_return_result_tuple[0]  # 成功
        # print('获取权限，typesql_return_result_tuple ========================', sql_return_result_tuple)
        msg = 'sql语句执行成功'
    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
        return 0  # 异常返回数字0
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    # 5.返回json格式的数据
    return result_int


# 功能：执行一条sql语句,返回tuple数据
# 1. sql 2. 参数后面的匹配变量
def execute_onesql_returntuple(sql, *args):
    # 初始化数据
    result_int = 0  # sql语句执行结果

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # print('sql语句为==', sql)
    # print("*args====", args)
    # print('参数args类型=={args}', type(args))

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
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("执行语句返回结果(类型)==", type(sql_return_result_tuple))  # tuple
        print("sql语句执行成功")

        # 拼接返回数据,返回列表
        msg = 'sql语句执行成功'
    except:
        # 如果发生错误则回滚
        print('sql语句执行失败')
        conn.rollback()
        return 0  # 异常返回数字0
    finally:
        # 不管是否异常，都关闭数据库连接
        cursor.close()
        conn.close()

    # 5.返回json格式的数据
    return sql_return_result_tuple


# 写入excel文件
"""
功能：写入excel文件
参数：path : excel文件的输出路径，结尾必须带上文件后缀,基于项目根目录的路径。如 根目录是“D:” excelrelapath = "test1.xlsx" ->最前面不用加\\
注意：1. excel文件名不存在会自动创建
     2. excel文件上级文件夹，如果不存在，不会自动创建
"""


def wirte2excelfile(excelrelpath):
    """
    # xlwt方式创建workbook
    # 创建sheet
    # sheet中写入数据
    # 保存excel
    book = xlwt.Workbook(encoding='utf-8')
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 0, 'haha')
    book.save('D:\\test1.xls')  # 需要写2个\\ xlsx 不支持xlsx格式文件
    """
    # XlsxWriter方式创建workbook
    excelabspath = rootdir + "\\" + excelrelpath
    print("excel文件绝对路径", excelabspath)
    book = xlsxwriter.Workbook(excelabspath)
    # book = xlsxwriter.Workbook("D:\\test1.xlsx")  # 必须使用双\\ 否则报参数错误

    # 创建sheet
    sheet1 = book.add_worksheet("Sheet1")
    # sheet中写入数据
    sheet1.write(0, 0, "ssss")
    sheet1.write(0, 1, "ssss")
    sheet1.write(0, 2, "ssss")
    # 关闭workbook
    book.close()


# 写入excel文件
"""
功能：写入excel文件
参数：1. excelrelpath : excel文件的输出路径(相对根目录的路径，路径前不用加\\)，结尾必须带上文件后缀,基于项目根目录的路径。如 根目录是“D:” excelrelapath = "test1.xlsx" ->最前面不用加\\
     2. searchsql : 查询语句
     2. ifwirte_th : 是否写入表头,默认是True,即写入表头
注意：1. excel文件名不存在会自动创建
     2. excel文件上级文件夹，如果不存在，不会自动创建
"""
def write2excelfile_returnjson_onesheet(excelrelpath, searchsql, ifwrite_th=True):
    # 1. 初始化json数据
    code = 500  # 默认失败
    count = 0  # sql语句执行结果个数
    data = {}
    buglist = []
    msg = '写入excel数据失败'

    # 2. 执行sql语句，获取返回值
    # sql = 'select bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, regression_times, reopen_times, submitterindex from bugcount.buglist'
    thtuples = execute_onesql_returnth(searchsql)
    print("====================thtuple=", thtuples)
    tdtuples = execute_onesql(searchsql)
    print("excel内容=========", tdtuples)

    # 3. 写入excel
    # XlsxWriter方式创建workbook
    excelabspath = rootdir + "\\" + excelrelpath
    print("excel绝对路径=", excelabspath)
    book = xlsxwriter.Workbook(excelabspath)
    sheet1 = book.add_worksheet("Sheet1")  # 写入哪个Sheet

    # 如果ifwrite_th = True,写入表头，写上字段信息,写入时将英文转成中文表头
    if ifwrite_th is True:
        for th in range(0, len(thtuples)):  # th是数字
            # print("表头", thtuples[th][0])
            # sheet1.write(0, th, thtuples[th][0])
            sheet1.write(0, th, tableheaddict[thtuples[th][0]])

    # 写入数据
    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(tdtuples) + 1):
        for col in range(0, len(thtuples)):
            if tdtuples[row - 1][col] is None or tdtuples[row - 1][col] == '':  # 表格内容是None,替换成空字符串
                sheet1.write(row, col, '')
            else:
                # 转换日期格式 ‘提交日期’列数从0开始
                if col == 0:
                    # 不为空的话，转成YYYY-MM-DD这种格式的,
                    # sheet1.write(row, col, datetime.strptime(tdtuples[row - 1][col], '%Y-%m-%d').date().strftime("%Y/%m/%d"))  # 导出前已经是日期格式，这样写法错误
                    # print("?????????????", tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                    # sheet1.write(row, col, tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                    sheet1.write(row, col, datetime.strftime(tdtuples[row - 1][col], "%Y/%#m/%#d"))  # 转成日期格式str

                # 将 ‘关闭情况’int--> 文字
                elif col == 8:  # 第9列是 ‘关闭情况’
                    # print('tdtuples[row - 1][col]type======================', type(tdtuples[row - 1][col])) # int
                    # print('tdtuples[row - 1][col]======================', tdtuples[row - 1][col])
                    if tdtuples[row - 1][col] == 1:
                        # tdtuples[row - 1][col] = '处理'  # 因为tuple 不能复制，所以这种写法错误，报错TypeError: 'tuple' object does not support item assignment
                        sheet1.write(row, col, '处理')
                    elif tdtuples[row - 1][col] == 2:
                        sheet1.write(row, col, '关闭')
                    elif tdtuples[row - 1][col] == 3:
                        sheet1.write(row, col, '回归')
                    elif tdtuples[row - 1][col] == 4:
                        sheet1.write(row, col, '延迟')
                    elif tdtuples[row - 1][col] == 5:
                        sheet1.write(row, col, '重开')
                    else:
                        sheet1.write(row, col, '未知')
                elif col == 9:  # 关闭时间
                    # 不为空
                    # print("?????????????当前值", tdtuples[row - 1][col])
                    # print("?????????????当前值type", type(tdtuples[row - 1][col]))
                    # print("?????????????", tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                    sheet1.write(row, col, tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                else:
                    sheet1.write(row, col, u'%s' % tdtuples[row - 1][col])  # 写入具体内容
    book.close()  # 必须关闭流，否则写不进去

    # 4. 重置json数据,顺序执行完就算陈公公
    code = 200
    msg = '写入excel数据成功'
    count = len(thtuples)

    # 5.返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


"""
功能：写入excel文件
参数：1. excelrelpath : excel文件的输出路径(相对根目录的路径，路径前不用加\\)，结尾必须带上文件后缀,基于项目根目录的路径。如 根目录是“D:” excelrelapath = "test1.xlsx" ->最前面不用加\\
     2. searchsql : 查询语句
     2. ifwirte_th : 是否写入表头,默认是True,即写入表头
注意：1. excel文件名不存在会自动创建
     2. excel文件上级文件夹，如果不存在，不会自动创建
"""
def write2excelfile_returnjson_nsheet(excelrelpath, searchsql, ifwrite_th=True):
    # 1. 初始化json数据
    code = 500  # 默认失败
    count = 0  # sql语句执行结果个数
    data = {}
    buglist = []
    msg = '写入excel数据失败'

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    get_project_sql = "select project from bugcount.buglist where project is not null and project != '' group by project"
    projects = execute_onesql_returntuple(get_project_sql)
    print("???????项目==", projects)

    # 2. 执行sql语句，获取返回值
    sql = 'select bug_submit_date, project, software, test_version, bug_description, severity_level, priority, ' \
          'bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, ' \
          'intermediate_situation, developer, remark, regression_times, reopen_times, submitterindex ' \
          'from bugcount.buglist '
    thtuples = execute_onesql_returnth(sql)
    print("====================thtuple=", thtuples)
    # tdtuples = execute_onesql(searchsql)
    # print("excel内容=========", tdtuples)

    # 3. 写入excel
    # XlsxWriter方式创建workbook
    excelabspath = rootdir + "\\" + excelrelpath
    print("excel绝对路径=", excelabspath)
    book = xlsxwriter.Workbook(excelabspath)

    # 返回的这种格式的 (('1808',), ('C8 3+4G',), ('FH03',), ('JC二期',), ('K项目',), ('K项目-多仓库',), ('K项目-马来',), ('K项目-鹰潭',), ('LJG',), ('WRJ',), ('ZG',), ('大S北向审计日志系统',), ('大S项目',), ('视频问题',))
    for i in projects:
        # print("!!!!!!!!项目==", i)
        index = projects.index(i)
        print("!!!!!!!!项目type==", i[0])
        print("!!!!!!!!项目type==", type(i[0]))
        # lsxwriter.exceptions.InvalidWorksheetName: Invalid Excel character '[]:*?/\' in sheetname 'K项目/K项目-多仓库'.
        # excel不支持sheet里写入带/的
        sheetN = book.add_worksheet(str(i[0]).replace('/', '-'))

        # 1. 每个表写入表头
        # 如果ifwrite_th = True,写入表头，写上字段信息,写入时将英文转成中文表头
        if ifwrite_th is True:
            for th in range(0, len(thtuples)):  # th是数字
                # print("表头", thtuples[th][0])
                # sheetN.write(0, th, thtuples[th][0])
                sheetN.write(0, th, tableheaddict[thtuples[th][0]])

        # 2. 获取表数据
        tdtuples = execute_onesql(searchsql, i[0])

        # 3.写入数据
        # 获取并写入数据段信息
        row = 1
        col = 0
        for row in range(1, len(tdtuples) + 1):
            for col in range(0, len(thtuples)):
                if tdtuples[row - 1][col] is None or tdtuples[row - 1][col] == '':  # 表格内容是None,替换成空字符串
                    sheetN.write(row, col, '')
                else:
                    # 转换日期格式 ‘提交日期’列数从0开始
                    if col == 0:
                        # 不为空的话，转成YYYY-MM-DD这种格式的,
                        # sheetN.write(row, col, datetime.strptime(tdtuples[row - 1][col], '%Y-%m-%d').date().strftime("%Y/%m/%d"))  # 导出前已经是日期格式，这样写法错误
                        # print("?????????????", tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                        # sheetN.write(row, col, tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                        sheetN.write(row, col, datetime.strftime(tdtuples[row - 1][col], "%Y/%#m/%#d"))  # 转成日期格式str

                    # 将 ‘关闭情况’int--> 文字
                    elif col == 8:  # 第9列是 ‘关闭情况’
                        # print('tdtuples[row - 1][col]type======================', type(tdtuples[row - 1][col])) # int
                        # print('tdtuples[row - 1][col]======================', tdtuples[row - 1][col])
                        if tdtuples[row - 1][col] == 1:
                            # tdtuples[row - 1][col] = '处理'  # 因为tuple 不能复制，所以这种写法错误，报错TypeError: 'tuple' object does not support item assignment
                            sheetN.write(row, col, '处理')
                        elif tdtuples[row - 1][col] == 2:
                            sheetN.write(row, col, '关闭')
                        elif tdtuples[row - 1][col] == 3:
                            sheetN.write(row, col, '回归')
                        elif tdtuples[row - 1][col] == 4:
                            sheetN.write(row, col, '延迟')
                        elif tdtuples[row - 1][col] == 5:
                            sheetN.write(row, col, '重开')
                        else:
                            sheetN.write(row, col, '未知')
                    elif col == 9:  # 关闭时间
                        # 不为空
                        # print("?????????????当前值", tdtuples[row - 1][col])
                        # print("?????????????当前值type", type(tdtuples[row - 1][col]))
                        # print("?????????????", tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                        sheetN.write(row, col, tdtuples[row - 1][col].strftime("%Y/%#m/%#d"))
                    else:
                        sheetN.write(row, col, u'%s' % tdtuples[row - 1][col])  # 写入具体内容
    book.close()  # 必须关闭流，否则写不进去

    # 4. 重置json数据,顺序执行完就算陈公公
    code = 200
    msg = '写入excel数据成功'
    count = len(thtuples)

    # 5.返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str




# 另存为到用户自定义文件，并写入excel文件
"""
功能：写入excel文件
参数：1. excelabspath : excel文件的输出绝对路径，结尾必须带上文件后缀,基于项目根目录的路径。如 根目录是“D:” excelrelapath = "test1.xlsx" ->最前面不用加\\
     2. searchsql : 查询语句
     2. ifwirte_th : 是否写入表头,默认是True,即写入表头
注意：1. excel文件名不存在会自动创建
     2. excel文件上级文件夹，如果不存在，不会自动创建
"""
def wirte2excelfile_storage_returnjson(excelabspath, searchsql, ifwrite_th=True):
     # 1. 初始化json数据
    code = 500  # 默认失败
    count = 0  # sql语句执行结果个数
    data = {}
    buglist = []
    msg = '写入excel数据失败'

    # 2. 执行sql语句，获取返回值
    # sql = 'select bug_submit_date, project, software, test_version, bug_description, severity_level, priority, bug_difficulty, bug_status, bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation, developer, remark, regression_times, reopen_times, submitterindex from bugcount.buglist'
    thtuples = execute_onesql_returnth(searchsql)
    print("====================thtuple=", thtuples)
    tdtuples = execute_onesql(searchsql)
    # print("excel内容=========", tdtuples)

    # 3. 写入excel
    # XlsxWriter方式创建workbook
    print("excel绝对路径=", excelabspath)
    book = xlsxwriter.Workbook(excelabspath)
    sheet1 = book.add_worksheet("Sheet1")  # 写入哪个sheet

    # 如果ifwrite_th = True,写入表头，写上字段信息,写入时将英文转成中文表头
    if ifwrite_th is True:
        for th in range(0, len(thtuples)):  # th是数字
            # print("表头", thtuples[th][0])
            # sheet1.write(0, th, thtuples[th][0])
            sheet1.write(0, th, tableheaddict[thtuples[th][0]])

    # 写入数据
    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(tdtuples) + 1):
        for col in range(0, len(thtuples)):
            if tdtuples[row - 1][col] is None:  # 表格内容是None,替换成空字符串
                sheet1.write(row, col, '')
            else:
                sheet1.write(row, col, u'%s' % tdtuples[row - 1][col])  # 写入具体内容
    book.close()  # 必须关闭流，否则写不进去

    # 4. 重置json数据,顺序执行完就算陈公公
    code = 200
    msg = '写入excel数据成功'
    count = len(thtuples)

    # 5.返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = buglist
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str
