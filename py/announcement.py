from py import utils
import pymysql
import json
import traceback  # 异常处理

#获取数据库配置
print('<admin.py> 获取。。。。。。。。。。。。。。。。config文件')
db_config_dict = utils.get_dbargs_from_config_byabspath()
# db_config_dict = utils.get_dbargs_from_config()

db_host = db_config_dict['db_host']
db_user = db_config_dict['db_user']
db_passwd = db_config_dict['db_passwd']
db_dbname = db_config_dict['db_dbname']
print('<admin.py>获取。。。。。。。。。。。。。。。。config文件 end ')


# 查询所有公告
def get_announcement():
    # 默认定义数据
    data = {}
    announcements = []
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        sql = 'select announcementid,announcement from announcement'
        print(f'sql语句为==', sql)

        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        # 执行语句，返回结果
        sql_return_result_tuple = cursor.fetchall()

        # 转换查询结果为[{},{},{}]这种格式的
        # print("执行语句返回结果：", sql_return_result_tuple)  # 返回元组
        # print("执行语句返回结果个数：", len(sql_return_result_tuple))  # 返回元组
        # print("sql语句执行成功")

        # 转化下查询结果为{},{},{}这种格式======================
        for r in sql_return_result_tuple:
            announcement = dict()
            announcement['announcementid'] = r[0]
            print('=============================r=', r)
            print('=============================announcementid', announcement['announcementid'])
            announcement['announcement'] = r[1]
            announcements.append(announcement)
        print('????dbutil 转换完的【{}】格式数据announcements==', announcements)

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
    data['data'] = announcements
    # 转化下查询结果为{},{},{}这种格式======================
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str


# 修改所有公告
def edit_announcement(argsjsonstr):
    # 默认定义数据
    data = {}
    announcements = []
    code = 500  # 默认失败
    msg = 'sql语句执行失败'
    count = 0  # sql语句执行结果个数

    # 解析参数
    print("================argsjsonstr", argsjsonstr)
    # argsobj = json.loads(argsjsonstr)
    announcement1_text = argsjsonstr["announcement1_text"]
    announcement2_text = argsjsonstr["announcement2_text"]
    announcement3_text = argsjsonstr["announcement3_text"]
    # print(announcement1_text)
    # print(announcement2_text)
    # print(announcement3_text)

    # 打开数据库连接
    conn = pymysql.connect(db_host, db_user, db_passwd, db_dbname)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 使用 execute()  方法执行 SQL 查询
    try:
        argslist = [announcement1_text, announcement2_text, announcement3_text]  # 只有值
        for r in argslist:
            announcementid = argslist.index(r) + 1
            print("---------------------------")
            print(r)
            sql = 'insert into announcement(announcementid,announcement) values(%s,%s) on duplicate key update announcement=%s'
            print(f'修改公告sql语句为==', sql)

            # 执行sql语句
            cursor.execute(sql, [announcementid, r, r])
            # 提交到数据库执行
            conn.commit()
            # 执行语句，返回结果
            sql_return_result_tuple = cursor.fetchall()
            print("============返回结果", sql_return_result_tuple)
            print(sql_return_result_tuple)
            print("sql语句执行成功")

            # 顺序执行完毕认为成功
            code = 200  # 成功
            msg = '修改公告sql语句执行成功'

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
    data['data'] = announcements
    # 转化下查询结果为{},{},{}这种格式======================
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('dbutil==jsonStr=====', json_str)
    return json_str