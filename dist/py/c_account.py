#MVC control层

#登陆注册相关业务,
# #python3自带hashlib 模块，直接导入
from py import dbutils
from py import utils
import json

#注册
def register(username_front, passwd_front):
    #前台传参数
    # json数据
    data = {}

    # 要返回的数据
    code = 500  # 返回给调用者的值，默认是500 Number类型的
    msg = '注册失败'
    count = 0
    regiser_sql_return_json_data = list()


    if username_front is not None and passwd_front is not None:
        print('==注册==，前台传的-username====', username_front)
        print('==注册==，前台传的-password====', passwd_front)

        # 查询数据是否有次username
        check_user_result_json = dbutils.check_username_is_registered(username_front)
        print('<dbutil查询回来josn==>', check_user_result_json)
        print('<dbutil查询回来josn==type ==>', type(check_user_result_json))
        # 获取查询到的个数,传的json全部都是字符串
        check_user_result_json_loads = json.loads(check_user_result_json)
        print('<c_account>?????????????????????josn count type = ', check_user_result_json_loads['count'])
        check_user_result_json_count = check_user_result_json_loads['count']
        if check_user_result_json_count > 0:
            print('此用户已存在')
            msg = '此用户已存在'
        else:
            print('此用户不存在')
            # 1. 加密passwd
            md5_passwd = utils.get_md5(passwd_front)

            """
            sql字段：
            userid: int
            username: str
            password: str
            user_remark: str
            user_email: str
            user_level: int (1-管理员 2 普通用户)
            create_time: date (2020-01-01这种格式)
            session: str
            """
            # 2. 加密结果存储
            # insert_passwd_sql = 'insert into bugcount.user values(null, %s, %s, null, null, null, null, null)'
            # insert_passwd_sql = 'select username from bugcount.user where username =%s'
            # 查看是否注册成功
            # 返回值为list 0位状态码 1位sql结果个数 2位为查询结果
            register_return_json = dbutils.register(username_front, md5_passwd)
            print('dbutil 执行返回结果=======', register_return_json)
            # 获取json后需要loads一下，转成字典形式
            register_return_json_loads = json.loads(register_return_json)

            #判断系统是否有此账号username
            if register_return_json_loads['code'] == 200:
                print('注册成功')
                code = register_return_json_loads['code']
                msg = '注册成功'
                count = register_return_json_loads['count']
                print('<c_account>=====json返回的data 类型是==《list》', type(register_return_json_loads['data']))
                regiser_sql_return_json_data = register_return_json_loads['data']

    else:
        print('用户名或密码为空，不做操作')

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = regiser_sql_return_json_data
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('《c_account》返回json==jsonStr=====', json_str)
    return json_str


#登录
def login(username_front, passwd_front):
    #前台传参数
    # json数据
    data = {}

    # 要返回的数据
    code = 500  # 返回给调用者的值，默认是500 Number类型的
    msg = '登录失败'
    count = 0
    login_sql_return_json_data = list()


    if username_front is not None and passwd_front is not None:
        print('==登录==，前台传的-username====', username_front)
        print('==登录==，前台传的-password====', passwd_front)

        print('此用户不存在,可登录，严重密码是否正确')
        # 1. 加密passwd
        md5_passwd = utils.get_md5(passwd_front)
        print('c_acount 转移出来的md5=', md5_passwd)

        """
        sql字段：
        userid: int
        username: str
        password: str
        user_remark: str
        user_email: str
        user_level: int (1-管理员 2 普通用户)
        create_time: date (2020-01-01这种格式)
        session: str
        """

        #获取json数据 jsonloads json -> 字典
        login_return_json = dbutils.login(username_front, md5_passwd)
        print('dbutil 执行返回结果=======', login_return_json)
        # 获取json后需要loads一下，转成字典形式
        login_return_json_loads = json.loads(login_return_json)

        #判断系统是否有此账号username
        if login_return_json_loads['code'] == 200:
            print('登录成功')
            code = login_return_json_loads['code']
            msg = login_return_json_loads['msg']
            count = login_return_json_loads['count']
            print('<c_account>=====json返回的data 类型是==《list》', type(login_return_json_loads['data']))
            login_sql_return_json_data = login_return_json_loads['data']

    else:
        print('用户名或密码为空，不做操作')

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = login_sql_return_json_data
    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)
    print('《c_account》返回json==jsonStr=====', json_str)
    return json_str



#测试方法
def test(username_front, passwd_front):
    #前台传参数

    # 要返回的数据
    code = 500  # 返回给调用者的值，默认是500 Number类型的
    msg = '注册失败'
    count = 0
    data = []  # 默认是一个list形式的
    if username_front is not None and passwd_front is not None:
            print('==注册==，前台传的-username====', username_front)
            print('==注册==，前台传的-password====', passwd_front)

            # 1. 加密passwd
            md5_passwd = utils.get_md5(passwd_front)

            """
            sql字段：
            userid: int
            username: str
            password: str
            user_remark: str
            user_email: str
            user_level: int (1-管理员 2 普通用户)
            create_time: date (2020-01-01这种格式)
            session: str
            """
            # 2. 加密结果存储
            # insert_passwd_sql = 'insert into bugcount.user values(null, %s, %s, null, null, null, null, null)'
            insert_passwd_sql = 'select username from bugcount.user where username =%s'
            # 查看是否注册成功
            # 返回值为list 0位状态码 1位sql结果个数 2位为查询结果
            return_list = dbutils.execute_db_onesql(insert_passwd_sql, username_front, md5_passwd)
            print('dbutil 执行返回结果=======', return_list)

            #判断系统是否有此账号username
            print('注册成功')
            code = return_list[0]
            msg = '注册成功'
            count = return_list[2]
            data = return_list[3]
            print("??????????????????????????执行sql返回的tuple==", return_list[3])


    #需要返回查询的sql数量，和查询结果
    #返回一个num型的成功或者失败
    return_list = [code, msg, count, data]
    print(f'注册方法返回结果list=={return_list}')
    return return_list
