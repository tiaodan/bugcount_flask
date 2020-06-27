from flask import Flask, render_template, request, redirect, url_for, Blueprint, send_from_directory
from py import c_account
from py import dbutils
import json
from py import admin
from py import utils
from py import buglist
import os
import pymysql
import time
from datetime import datetime

'''
出现该问题主要原因是新版的flask抛弃了flask.ext这种引入扩展的方法，更改为 flask_扩展名
ModuleNotFoundError: No module named 'flask.ext' 的解决方法
以前：from flask.ext.script import Manager
现在：from flask_script import Manager
'''
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin

#设置static_folder='.', static_url_path='' 表示从根目录查找文件


app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
# app = Flask(__name__, static_folder='.', static_url_path='')

# 给登录用户初始化一个id, 默认是1
user_id = 1


# 保持登录相关
# 保持登录需要 创建一个User类
class User(UserMixin):
    def is_authenticated(self): # 是否鉴权
        return True

    def is_active(self):  # 是否激活
        return True

    def is_anonymous(self): # 是否匿名
        return False

    def get_id(self): # 定义默认id
        return '1'


#   flask_login
app.secret_key = 'sunkaisens' # 设置
login_manager = LoginManager()
# login_manager.session_protection = 'Strong'  # 保护等级
# login_manager.session_protection = 'basic'  # 保护等级
login_manager.session_protection = None  # 保护等级

login_manager.login_view = '/'  # 登录网页路径
login_manager.init_app(app)


# 这个必须加
@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user


@app.route('/test')
def test():
    return  app.send_static_file('pages/test2.html')


@app.route('/')
def hello_world():
    # return 'Hello World!'
    # return app.send_static_file('pages/register.html')
    return app.send_static_file('pages/login.html')
    # return render_template('login-nojs.html')
    # return render_template('pages/test2.html')

#注册界面入口
@app.route('/registerView')
def register_view():
    return app.send_static_file('pages/register.html')


#登录界面入口
@app.route('/loginView')
def login_view():
    return app.send_static_file('pages/login.html')




#主界面入口,给主界面加登录验证
@app.route('/indexView')
@login_required
def index_view():
    return app.send_static_file('index.html')

# 指定请求方式，如果不指定，则无法匹配到请求
@app.route("/register", methods=("GET", "POST"))
def register():

    #构造要返回的字符串# 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    """
    :return:
    {
    "code": 0,
    "msg": "",
    "count": 29,
    "data": []
}
    """
    code = 500
    print('??????????????code type=', type(code))
    msg = '注册失败，请重新尝试'
    count = 0
    regiser_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====注册===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)

        # 获取数据并转化成字典
        # user_info = request.form.to_dict()
        # print('type-username = ', type(user_info.get("username")))
        # if user_info.get("username") == "admin" and user_info.get("password") == '123456':
        #     return redirect("/")

        username = request.form.get('username')
        password = request.form.get('password')
        print('获取到的参数 ==', username, password)

        # 账号或密码不能为空
        if username is not None and password is not None:
            if username.strip() == '' or password.strip() == '':
                msg = '用户名或密码为空'
            else:
                register_return_json = c_account.register(username, password)
                # 判断执行结果,我只要成功或者失败就可以了
                # 获取到json需要解析
                register_return_json_loads = json.loads(register_return_json)
                if register_return_json_loads['code'] == 200:
                    code = register_return_json_loads['code']
                    msg = '注册成功'
                    count = register_return_json_loads['count']
                    regiser_sql_return_json_data = register_return_json_loads['data']
                if register_return_json_loads['code'] == 500:
                    msg = register_return_json_loads['msg']  # 此用户已存在

        else:
            msg = '用户名或密码为空，不做操作'
            print('用户名或密码为空，不做操作')


    #什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = regiser_sql_return_json_data
    print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《c_account》返回json==jsonStr=====', json_str)
    return json_str



# 登录界面,# 指定请求方式，如果不指定，则无法匹配到请求
# 指定请求方式，如果不指定，则无法匹配到请求
@app.route("/login", methods=("GET", "POST"))
def login():

    #构造要返回的字符串# 初始化返回的数据 [arg1, arg2, arg3, arg4] arg1=状态码（num）arg2=msg(str) arg3= count(num) arg4=tuple
    """
    :return:
    {
    "code": 0,
    "msg": "",
    "count": 29,
    "data": []
}
    """
    code = 500
    print('??????????????code type=', type(code))
    msg = '登录失败，请重新尝试'
    count = 0
    login_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====登录===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)

        # 获取数据并转化成字典
        # user_info = request.form.to_dict()
        # print('type-username = ', type(user_info.get("username")))
        # if user_info.get("username") == "admin" and user_info.get("password") == '123456':
        #     return redirect("/")

        username = request.form.get('username')
        password = request.form.get('password')
        print('获取到的参数 ==', username, password)

        # 账号或密码不能为空
        if username is not None and password is not None:
            if username.strip() == '' or password.strip() == '':
                msg = '用户名或密码为空'
            else:
                login_return_json = c_account.login(username, password)
                # 判断执行结果,我只要成功或者失败就可以了
                # 获取到json需要解析
                login_return_json_loads = json.loads(login_return_json)

                code = login_return_json_loads['code']
                msg = login_return_json_loads['msg']
                count = login_return_json_loads['count']
                login_sql_return_json_data = login_return_json_loads['data']
                # 返回200 ok 并且查询到用户（count>0 ）才算成功
                if code == 200 and count > 0:
                    msg = '登录成功'
                #     添加登录记录，前端session保存
                    user = User()
                    print("app.py登录成功，保存的user====", user)
                    print("app.py登录成功，保存的user.userid====", user.get_id())
                    login_user(user)

                    # 登录成功的话，不在前台跳转，在后台跳转

                    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>跳转界面")
                    # return app.send_static_file('index.html')
                    # return redirect('/indexView')

                if login_return_json_loads['code'] == 500:
                    msg = login_return_json_loads['msg']  # 此用户已存在

        else:
            msg = '用户名或密码为空，不做操作'
            print('用户名或密码为空，不做操作')


    #什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = login_sql_return_json_data
    print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《c_account》返回json==jsonStr=====', json_str)
    return json_str

# 登录界面,# 指定请求方式，如果不指定，则无法匹配到请求
# 指定请求方式，如果不指定，则无法匹配到请求
@app.route("/logout", methods=("GET", "POST"))
def logout():
#     添加登出记录，前端session保存
    user = load_user(user_id)
    logout_user()
    print("app.py登出成功，保存的user====", user)
    print("app.py登出成功，保存的user。id====", user.get_id())

    # 跳转登录界面
    return app.send_static_file('pages/login.html')






#test getUserList
@app.route('/getUserList', methods=("GET", "POST"))
def getUserList():
    print('获取用户列表')
    if request.method == "GET":
        page = int(request.args.get('page'))
        limit = int(request.args.get('limit'))
        print(f'??????????????????????????????????参数{page} , {limit}')
        print('??????????????????????????????????参数type{page} , {limit},传过来的是字符串', type(page), type(limit))
        # 获取请求的页码， 和每页个数
        json_str = admin.search_users(page, limit)
        return json_str

#post 添加用户
@app.route('/addUser', methods=("GET", "POST"))
def addUser():
    print('<app.py> 添加用户')

    code = 500
    print('??????????????code type=', type(code))
    msg = '添加用户失败，请重新尝试'
    count = 0
    adduser_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====注册===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)

        # 获取数据并转化成字典
        # user_info = request.form.to_dict()
        # print('type-username = ', type(user_info.get("username")))
        # if user_info.get("username") == "admin" and user_info.get("password") == '123456':
        #     return redirect("/")

        #需要获取的参数 username, password, user_remark, user_email, user_level, create_time, session
        username = request.form.get('username')
        password = request.form.get('password')
        user_remark = request.form.get('user_remark')
        user_email = request.form.get('user_email')
        user_level = request.form.get('user_level')
        print('???????????????user level===============================', user_level)
        create_time = request.form.get('create_time')
        session = request.form.get('session')

        # 密码需要md5加密
        # 1. 加密passwd
        md5_passwd = utils.get_md5(password)


        print('获取到的参数 ==', username, password)

        # 账号或密码不能为空
        if username is not None and password is not None:
            if username.strip() == '' or password.strip() == '':
                msg = '用户名或密码为空'
            else:
                # 执行sql
                adduser_return_json = admin.add_user(username, md5_passwd, user_remark, user_email, user_level, create_time, session)
                # 判断执行结果,我只要成功或者失败就可以了
                # 获取到json需要解析
                adduser_return_json_loads = json.loads(adduser_return_json)
                if adduser_return_json_loads['code'] == 200:
                    code = adduser_return_json_loads['code']
                    msg = '添加用户成功'
                    count = adduser_return_json_loads['count']
                    adduser_sql_return_json_data = adduser_return_json_loads['data']
                if adduser_return_json_loads['code'] == 500:
                    msg = adduser_return_json_loads['msg']  # 此用户已存在

        else:
            msg = '用户名或密码为空，不做操作'
            print('用户名或密码为空，不做操作')

    # 什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = adduser_sql_return_json_data
    print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《app.py》返回json==jsonStr=====', json_str)
    return json_str

#post 删除用户
@app.route('/delUser', methods=("GET", "POST"))
def delUser():
    print('<app.py> 删除单个用户')

    code = 500
    print('??????????????code type=', type(code))
    msg = '删除用户失败，请重新尝试'
    count = 0
    deluser_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====注册===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)

        # 获取数据并转化成字典
        # user_info = request.form.to_dict()
        # print('type-username = ', type(user_info.get("username")))
        # if user_info.get("username") == "admin" and user_info.get("password") == '123456':
        #     return redirect("/")

        #需要获取的参数 userid 根据userid删除
        userid = request.values.get('userid')
        print('获取到的参数 userid ==', userid)

        # 账号或密码不能为空
        if userid is not None:
            if userid.strip() == '':
                msg = 'userid为空'
            else:
                # 执行sql
                deluser_return_json = admin.del_user(userid)
                # 判断执行结果,我只要成功或者失败就可以了
                # 获取到json需要解析
                deluser_return_json_loads = json.loads(deluser_return_json)
                if deluser_return_json_loads['code'] == 200:
                    code = deluser_return_json_loads['code']
                    msg = '删除用户成功'
                    count = deluser_return_json_loads['count']
                    deluser_sql_return_json_data = deluser_return_json_loads['data']
                if deluser_return_json_loads['code'] == 500:
                    msg = deluser_return_json_loads['msg']  # 删除失败

        else:
            msg = 'userid为空，不做操作'
            print('userid为空，不做操作')

    # 什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = deluser_sql_return_json_data
    print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《app.py》返回json==jsonStr=====', json_str)
    return json_str

#post 编辑用户
@app.route('/editUser', methods=("GET", "POST"))
def editUser():
    print('<app.py> 编辑单个用户')

    code = 500
    print('??????????????code type=', type(code))
    msg = '编辑用户失败，请重新尝试'
    count = 0
    edituser_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====注册===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)

        #需要获取的参数 userid 根据userid删除,requst请求通过form 或者value都能拿到，因为requst里参数就是form
        userid = request.values.get('userid')
        print('获取到的参数 userid ==', userid)
        username = request.form.get('username')
        password = request.form.get('password')
        user_remark = request.form.get('user_remark')
        user_email = request.form.get('user_email')
        user_level = request.form.get('user_level')
        create_time = request.form.get('create_time')
        session = request.form.get('session')

        # 1. 加密passwd
        md5_passwd = utils.get_md5(password)

        # 账号或密码不能为空
        if userid is not None:
            if userid.strip() == '':
                msg = 'userid为空'
            else:
                # 执行sql ， 除了userid 和username 不能改，其他都能改
                edituser_return_json = admin.edit_user(userid, username, md5_passwd, user_remark, user_email, user_level, create_time, session)
                # 判断执行结果,我只要成功或者失败就可以了
                # 获取到json需要解析
                edituser_return_json_loads = json.loads(edituser_return_json)
                if edituser_return_json_loads['code'] == 200:
                    code = edituser_return_json_loads['code']
                    msg = '编辑用户成功'
                    count = edituser_return_json_loads['count']
                    edituser_sql_return_json_data = edituser_return_json_loads['data']
                if edituser_return_json_loads['code'] == 500:
                    msg = edituser_return_json_loads['msg']  # 编辑用户失败

        else:
            msg = 'userid为空，不做操作'
            print('userid为空，不做操作')

    # 什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = edituser_sql_return_json_data
    print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《app.py》返回json==jsonStr=====', json_str)
    return json_str


# #########################  bug操作相关  ############################################################################
#test getBugList
@app.route('/getBugList', methods=("GET", "POST"))
def getBugList():
    print('获取用户列表')
    if request.method == "GET":
        page = int(request.args.get('page'))
        limit = int(request.args.get('limit'))
        # 获取请求的页码， 和每页个数
        json_str = buglist.search_buglist(page, limit)
        return json_str
    if request.method == "POST":
        # 获取后台筛选数据
        print('getBugList 获取后台筛选条件 数据')
        request
        columns = request.args.get('columns')
        print('columns.type==', type(columns))
        # page = int(request.args.get('page'))
        # limit = int(request.args.get('limit'))
        # 获取请求的页码， 和每页个数
        # json_str = buglist.search_buglist_filter_args(page, limit, columns)
        json_str = '{"project": ["1801"],"bug_description": ["调度台无法强插"]}'
        return json_str




#post 新增bug
@app.route('/addBug', methods=("GET", "POST"))
def addBug():
    print('<app.py> 新增单个bug')

    code = 500
    print('??????????????code type=', type(code))
    msg = '新增bug失败，请重新尝试'
    count = 0
    addbug_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====注册===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)

        # 解析前台传的参数
        # 1
        # bugid = request.form.get('bugid')
        # print('获取到的参数 userid ==', bugid) -
        bug_submit_date = request.form.get('bug_submit_date')
        project = request.form.get('project')
        software = request.form.get('software')
        test_version = request.form.get('test_version')

        # 2
        bug_description = request.form.get('bug_description')
        severity_level = request.form.get('severity_level')
        priority = request.form.get('priority')
        bug_difficulty = request.form.get('bug_difficulty')
        bug_status = request.form.get('bug_status')

        # 3
        bug_close_date = request.form.get('bug_close_date')
        close_version = request.form.get('close_version')
        cause_analysis = request.form.get('cause_analysis')
        bug_img = request.form.get('bug_img')
        intermediate_situation = request.form.get('intermediate_situation')

        # 4
        developer = request.form.get('developer')
        remark = request.form.get('remark')
        first_bug_regression_date = request.form.get('first_bug_regression_date')
        first_bug_regression_status = request.form.get('first_bug_regression_status')
        first_bug_regression_remark = request.form.get('first_bug_regression_remark')

        # 5
        second_bug_regression_date = request.form.get('second_bug_regression_date')
        second_bug_regression_status = request.form.get('second_bug_regression_status')
        second_bug_regression_remark = request.form.get('second_bug_regression_remark')
        third_bug_regression_date = request.form.get('third_bug_regression_date')
        third_bug_regression_status = request.form.get('third_bug_regression_status')
        third_bug_regression_remark = request.form.get('third_bug_regression_remark')



        # 账号或密码不能为空

        # 执行sql ， 除了bugid，其他都能改
        """
        参数(bugid, bug_submit_date, project, software, test_version
           , bug_description, severity_level, priority, bug_difficulty, bug_status
           , bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation
           , developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark
           , second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark
           , third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark)
        """
        # 25个参数 不包括bugid, bugid在数据库中自增
        addbug_return_json = buglist.add_bug(bug_submit_date, project, software, test_version
                                               , bug_description, severity_level, priority, bug_difficulty,
                                               bug_status
                                               , bug_close_date, close_version, cause_analysis, bug_img,
                                               intermediate_situation
                                               , developer, remark, first_bug_regression_date,
                                               first_bug_regression_status, first_bug_regression_remark
                                               , second_bug_regression_date, second_bug_regression_status,
                                               second_bug_regression_remark
                                               , third_bug_regression_date, third_bug_regression_status,
                                               third_bug_regression_remark)

        # 判断执行结果,我只要成功或者失败就可以了
        # 获取到json需要解析
        addbug_return_json_loads = json.loads(addbug_return_json)
        if addbug_return_json_loads['code'] == 200:
            code = addbug_return_json_loads['code']
            msg = '新增用户成功'
            count = addbug_return_json_loads['count']
            addbug_sql_return_json_data = addbug_return_json_loads['data']
        if addbug_return_json_loads['code'] == 500:
            msg = addbug_return_json_loads['msg']  # 编辑用户失败


    # 什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = addbug_sql_return_json_data
    print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《app.py》返回json==jsonStr=====', json_str)
    return json_str

#post 删除bug
@app.route('/delBug', methods=("GET", "POST"))
def delBug():
    print('<app.py> 删除单个bgu')

    code = 500
    msg = '删除bug失败，请重新尝试'
    count = 0
    delbug_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====注册===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)


        #需要获取的参数 userid 根据userid删除
        bugid = request.values.get('bugid')
        print('获取到的参数 bugid ==', bugid)

        # 账号或密码不能为空
        if bugid is not None:
            if bugid.strip() == '':
                msg = 'userid为空'
            else:
                # 执行sql
                delbug_return_json = buglist.del_bug(bugid)
                # 判断执行结果,我只要成功或者失败就可以了
                # 获取到json需要解析
                delbug_return_json_loads = json.loads(delbug_return_json)
                if delbug_return_json_loads['code'] == 200:
                    code = delbug_return_json_loads['code']
                    msg = '删除用户成功'
                    count = delbug_return_json_loads['count']
                    delbug_sql_return_json_data = delbug_return_json_loads['data']
                if delbug_return_json_loads['code'] == 500:
                    msg = delbug_return_json_loads['msg']  # 删除失败

        else:
            msg = 'userid为空，不做操作'
            print('userid为空，不做操作')

    # 什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = delbug_sql_return_json_data
    print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《app.py》返回json==jsonStr=====', json_str)
    return json_str


#post 清空buglist
@app.route('/truncateTableBuglist', methods=("GET", "POST"))
def truncateTableBuglist():
    print('<app.py> 清空数据buglist')

    json_str = buglist.truncate_table_buglist()
    print('《app.py》truncateTableBuglist 返回jsonStr==', json_str)
    return json_str

#post 编辑bug
@app.route('/editBug', methods=("GET", "POST"))
def editBug():
    print('<app.py> 编辑单个bug')

    code = 500
    print('??????????????code type=', type(code))
    msg = '编辑bug失败，请重新尝试'
    count = 0
    editbug_sql_return_json_data = list()

    # json数据
    data = {}

    # GET请求
    if request.method == "GET":
        print('get请求')
        msg = 'get请求,不处理'
    # POST请求
    if request.method == "POST":
        print("====注册===== - post请求")
        print('requets.header=', request.headers)
        print('equest.json', request.json)
        print('equest.date', request.data)

        #解析前台传的参数
        # 1
        bugid = request.form.get('bugid')
        print('获取到的参数 userid ==', bugid)
        bug_submit_date = request.form.get('bug_submit_date')
        project = request.form.get('project')
        software = request.form.get('software')
        test_version = request.form.get('test_version')

        #2
        bug_description = request.form.get('bug_description')
        severity_level = request.form.get('severity_level')
        priority = request.form.get('priority')
        bug_difficulty = request.form.get('bug_difficulty')
        bug_status = request.form.get('bug_status')


        # 3
        bug_close_date = request.form.get('bug_close_date')
        close_version = request.form.get('close_version')
        cause_analysis = request.form.get('cause_analysis')
        bug_img = request.form.get('bug_img')
        intermediate_situation = request.form.get('intermediate_situation')


        # 4
        developer = request.form.get('developer')
        remark = request.form.get('remark')
        first_bug_regression_date = request.form.get('first_bug_regression_date')
        first_bug_regression_status = request.form.get('first_bug_regression_status')
        first_bug_regression_remark = request.form.get('first_bug_regression_remark')

        # 5
        second_bug_regression_date = request.form.get('second_bug_regression_date')
        second_bug_regression_status = request.form.get('second_bug_regression_status')
        second_bug_regression_remark = request.form.get('second_bug_regression_remark')
        third_bug_regression_date = request.form.get('third_bug_regression_date')
        third_bug_regression_status = request.form.get('third_bug_regression_status')
        third_bug_regression_remark = request.form.get('third_bug_regression_remark')



        # 账号或密码不能为空
        if bugid is not None:
            if bugid.strip() == '':
                msg = 'bugid 为空'
            else:
                # 执行sql ， 除了bugid，其他都能改
                """
                参数(bugid, bug_submit_date, project, software, test_version
                   , bug_description, severity_level, priority, bug_difficulty, bug_status
                   , bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation
                   , developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark
                   , second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark
                   , third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark)
                """
                editbug_return_json = buglist.edit_bug(bugid, bug_submit_date, project, software, test_version
                                                       , bug_description, severity_level, priority, bug_difficulty, bug_status
                                                       , bug_close_date, close_version, cause_analysis, bug_img, intermediate_situation
                                                       , developer, remark, first_bug_regression_date, first_bug_regression_status, first_bug_regression_remark
                                                       , second_bug_regression_date, second_bug_regression_status, second_bug_regression_remark
                                                       , third_bug_regression_date, third_bug_regression_status, third_bug_regression_remark)

                # 判断执行结果,我只要成功或者失败就可以了
                # 获取到json需要解析
                editbug_return_json_loads = json.loads(editbug_return_json)
                if editbug_return_json_loads['code'] == 200:
                    code = editbug_return_json_loads['code']
                    msg = '编辑用户成功'
                    count = editbug_return_json_loads['count']
                    editbug_sql_return_json_data = editbug_return_json_loads['data']
                if editbug_return_json_loads['code'] == 500:
                    msg = editbug_return_json_loads['msg']  # 编辑用户失败

        else:
            msg = 'userid为空，不做操作'
            # print('userid为空，不做操作')

    # 什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = editbug_sql_return_json_data
    # print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《app.py》编辑单个bug 返回jsonStr== ', json_str)
    return json_str


# ###################统计列表方法
#test getBugCountByProject
@app.route('/getBugCountByProject', methods=("GET", "POST"))
def getBugCountByProject():
    print('获取bug统计信息')
    print('解析前台传的参数')
    startTime = request.values.get('startTime')
    endTime = request.values.get('endTime')

    if request.method == "GET":
        # 获取请求的开始使劲按， 和结束时间
        print('《app.py》 getBugCountByProject 前台参数 startime endTime==', startTime, endTime)
        json_str = buglist.get_bugcount_by_project(startTime, endTime)
        return json_str
    if request.method == "POST":
        # 获取请求的开始使劲按， 和结束时间
        print('《app.py》 getBugCountByProject startime endTime==', startTime, endTime)
        json_str = buglist.get_bugcount_by_project(startTime, endTime)
        return json_str


# 获取 项目维度 按时间排序的数据
# get_bugcount_by_project_orderby_time
# getBugcountByProjectOrderbyTime
@app.route('/getBugcountByProjectOrderbyTime', methods=("GET", "POST"))
def get_bugcount_by_project_orderby_time():
    # print('《app.py》 获取项目bugcount 前台参数  get_bugcount_by_project_orderby_time')
    # print('解析前台传的参数')
    startTime = request.values.get('startTime')
    endTime = request.values.get('endTime')

    if request.method == "POST":
        # 获取请求的开始使劲按， 和结束时间
        print('《app.py》 获取项目bugcount 前台参数 startime endTime==', startTime, endTime)
        json_str = buglist.get_bugcount_by_project(startTime, endTime)
        return json_str

#test getBugCountByProject
@app.route('/getBugCountByDeveloper', methods=("GET", "POST"))
def getBugCountByDeveloper():
    print('获取bug统计信息')
    print('解析前台传的参数')
    startTime = request.values.get('startTime')
    endTime = request.values.get('endTime')

    if request.method == "GET":
        # 获取请求的开始使劲按， 和结束时间
        print('《app.py》 获取开发bugcount 到的前台 参数 startime endTime==', startTime, endTime)
        json_str = buglist.get_bugcount_by_developer(startTime, endTime)
        return json_str
    if request.method == "POST":
        # 获取请求的开始使劲按， 和结束时间
        print('《app.py》 获取开发bugcount 到的前台 参数 startime endTime==', startTime, endTime)
        json_str = buglist.get_bugcount_by_developer(startTime, endTime)
        return json_str


#test downloadBuglistTemplate 文件下载
@app.route('/downloadBuglistTemplate', methods=("GET", "POST"))
def downloadBuglistTemplate():
    print('文件下载')
    return send_from_directory(r"excel_upload", filename="template.xls", as_attachment=True)


@app.route('/uploadBuglist', methods=['POST', 'GET'])
def uploadBuglist():
    code = 500
    print('??????????????code type=', type(code))
    msg = '编辑bug失败，请重新尝试'
    count = 0
    editbug_sql_return_json_data = list()

    # json数据
    data = {}
    jsondata = list()
    print('uplaod')
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        # upload_path = os.path.join(basepath, 'excel_upload',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        upload_path = os.path.join(basepath, 'excel_upload', f.filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        print('上传文件目录==', upload_path)
        # 如果存在着重名文件，先删除
        if os.path.exists(upload_path):
            print('删除同名文件')
            os.remove(upload_path)

        f.save(upload_path)
        code = 200
        msg = '文件上传成功'

    # 什么条件都不符合，返回失败
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = jsondata
    # print('未转化json前的数据， ===', data)

    # 转化下查询结果为{},{},{}这种格式======================
    json_str = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False传回utf8
    print('《app.py》 上传文件，返回json==jsonStr=====', json_str)
    return json_str


#导入数据
@app.route('/importMysqlByExcel', methods=['POST', 'GET'])
def importMysqlByExcel():

    json_str = dbutils.import_mysql_by_excel()
    print('《app.py》返回json==jsonStr=====', json_str)
    return json_str

# 为了画折线图 获取所有项目的数据 get
@app.route('/getTableForDrawMapWithProject', methods=['POST', 'GET'])
def getTableForDrawMapWithProject():
    # 获取前台传的参数
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    print(f"《app.py》画折线图 所有项目的数据，前台传的参数{startTime}， {endTime}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_allprojectdata_withproject_orderby_date(startTime, endTime)
        print('《app.py》画折线图 获取所有项目的数据, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_allprojectdata_withproject_orderby_date(startTime, endTime)
        print('《app.py》画折线图 获取所有项目的数据, 返回json==jsonStr=====', json_str)

    return json_str


# 为了画折线图 获取新增bug(status=1) 今天相对昨天的增长和关闭情况
@app.route('/getTableForDrawMapWithProjectALongtimeNewBugAddAndClose', methods=['POST', 'GET'])
def getTableForDrawMapWithProjectALongtimeNewBugAddAndClose():
    # 获取前台传的参数
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    timeDifference = int(request.values.get("timeDifference"))
    print(f'timeDifference 类型{type(timeDifference)}')  # str
    print(f"《app.py》新增bug，前台传的参数startime={startTime}， endtime={endTime}, timeDifference={timeDifference}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_allprojectdata_withproject_alongtime_newbug_addandclose_orderby_date(startTime, endTime, timeDifference)
        print('《app.py》画折线图 获取新增bug(status=1) 今天相对昨天的增长和关闭情况, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_allprojectdata_withproject_alongtime_newbug_addandclose_orderby_date(startTime, endTime, timeDifference)
        print('《app.py》画折线图 获取新增bug(status=1) 今天相对昨天的增长和关闭情况, 返回json==jsonStr=====', json_str)

    return json_str



# 为了画折线图 获取所有项目 每日累加的数据 get
@app.route('/getTableForDrawMapWithProjectEverydaySum', methods=['POST', 'GET'])
def getTableForDrawMapWithProjectEverydaySum():
    # 获取前台传的参数
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    print(f"前台传的参数{startTime}， {endTime}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_allprojectdata_everyday_sum_withproject_orderby_date(startTime, endTime)
        print('《app.py》画折线图 获取所有项目的数据, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_allprojectdata_everyday_sum_withproject_orderby_date(startTime, endTime)
        print('《app.py》画折线图 获取所有项目的数据, 返回json==jsonStr=====', json_str)

    return json_str

# 为了画折线图 获取全部bug 绘制全部bug增长曲线和关闭； + bug剩余情况
@app.route('/getTableForDrawMapWithProjectALongtimeAllBug', methods=['POST', 'GET'])
def getTableForDrawMapWithProjectALongtimeAllBug():
    # 获取前台传的参数
    print(request.values)
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    timeDifference = int(request.values.get("timeDifference"))
    print(f'timeDifference 类型{type(timeDifference)}')  # str
    print(f"《app.py》全部bug，前台传的参数startime={startTime}， endtime={endTime}, timeDifference={timeDifference}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_allprojectdata_withproject_alongtime_allbug_orderby_date(startTime, endTime, timeDifference)
        print('《app.py》画折线图 获取全部bug 一段时间内的的增长和关闭情况, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_allprojectdata_withproject_alongtime_allbug_orderby_date(startTime, endTime, timeDifference)
        print('《app.py》画折线图 获取全部bug 一段时间内的的增长和关闭情况, 返回json==jsonStr=====', json_str)

    return json_str


# 为了画折线图 获取所有 开发的数据 get
@app.route('/getTableForDrawMapWithDeveloper', methods=['POST', 'GET'])
def getTableForDrawMapWithDeveloper():
    # 获取前台传的参数
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    print(f"《app.py》获取所有 开发的数据，前台传的参数{startTime}， {endTime}")

    json_str = ''

    # 默认get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_allprojectdata_withdeveoper_orderby_date(startTime, endTime)
        print('《app.py》画折线图 获取所有开发的数据, 返回json==jsonStr=====', json_str)

    return json_str


# #######  开发维度 start########################
# 获取开发维度 所有bug /1-2级别bug 情况
@app.route('/getTableWithDeveloper', methods=['POST', 'GET'])
def getTableWithDeveloper():
    # 获取前台传的参数
    print(request.values)
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    timeDifference = int(request.values.get("timeDifference"))
    print(f'timeDifference 类型{type(timeDifference)}')  # str
    print(f"《app.py。开发维度》bug table，前台传的参数startime={startTime}， endtime={endTime}, timeDifference={timeDifference}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_table_withdeveloper_orderby_date(startTime, endTime, timeDifference)
        print('《app.py。开发维度》bug table, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_table_withdeveloper_orderby_date(startTime, endTime, timeDifference)
        print('《app.py。开发维度》bug table, 返回json==jsonStr=====', json_str)

    return json_str



# 为了画折线图 开发维度 获取全部bug 绘制全部bug增长曲线和关闭； + bug剩余情况 （增长是一周增长，关闭是累计关闭，剩余是累计剩余）
@app.route('/getTableForDrawMapWithDeveloperALongtimeAllBug', methods=['POST', 'GET'])
def getTableForDrawMapWithDeveloperALongtimeAllBug():
    # 获取前台传的参数
    print(request.values)
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    timeDifference = int(request.values.get("timeDifference"))
    print(f'timeDifference 类型{type(timeDifference)}')  # str
    print(f"《app.py，开发维度》全部bug折线图，前台传的参数startime={startTime}， endtime={endTime}, timeDifference={timeDifference}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_alldeveloperdata_withdeveloper_alongtime_allbug_orderby_date(startTime, endTime, timeDifference)
        print('《app.py，开发维度》全部bug折线图,获取全部bug 一段时间内的的增长和关闭情况, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('post请求')
        json_str = buglist.get_alldeveloperdata_withdeveloper_alongtime_allbug_orderby_date(startTime, endTime, timeDifference)
        print('《app.py，开发维度》全部bug折线图,获取全部bug 一段时间内的的增长和关闭情况, 返回json==jsonStr=====', json_str)

    return json_str


# 为了画折线图 7）开发维度，按时间（时间可自定义），按照一定时间颗粒度（时间可自定义），绘制新增bug增长曲线和关闭曲线；
@app.route('/getTableForDrawMapWithDeveloperALongtimeAddBugAddAndClose', methods=['POST', 'GET'])
def getTableForDrawMapWithDeveloperALongtimeAddBugAddAndClose():
    # 获取前台传的参数
    print(request.values)
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    timeDifference = int(request.values.get("timeDifference"))
    print(f'timeDifference 类型{type(timeDifference)}')  # str
    print(f"《app.py，开发维度》新增bug增长曲线和关闭曲线，前台传的参数startime={startTime}， endtime={endTime}, timeDifference={timeDifference}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_alldeveloperdata_withdeveloper_alongtime_addandclosebug_orderby_date(startTime, endTime, timeDifference)
        print('《app.py，开发维度》新增bug增长曲线和关闭曲线 一段时间内的的增长和关闭情况, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('post请求')
        json_str = buglist.get_alldeveloperdata_withdeveloper_alongtime_addandclosebug_orderby_date(startTime, endTime, timeDifference)
        print('《app.py，开发维度》新增bug增长曲线和关闭曲线 一段时间内的的增长和关闭情况, 返回json==jsonStr=====', json_str)

    return json_str


# 9）开发维度，按时间（时间可自定义）统计软件自测考量：相比较这段时间产生的所有bug，易bug产生比率；
@app.route('/getEasyBugTableWithDeveloper', methods=['POST', 'GET'])
def getEasyBugTableWithDeveloper():
    # 获取前台传的参数
    print(request.values)
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    print(f"《app.py。开发维度》易bug table，前台传的参数startime={startTime}， endtime={endTime}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_easybug_table_withdeveloper_orderby_date(startTime, endTime)
        print('《app.py。开发维度》易bug table, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_easybug_table_withdeveloper_orderby_date(startTime, endTime)
        print('《app.py。开发维度》易bug table, 返回json==jsonStr=====', json_str)

    return json_str


# 11）开发维度，按时间（时间可自定义），按照一定时间颗粒度（时间可自定义），绘制易bug产生比率曲线；1/2    月/周/季
@app.route('/getEasyBugTableForDrawMapWithDeveloper', methods=['POST', 'GET'])
def getEasyBugTableForDrawMapWithDeveloper():
    # 获取前台传的参数
    print(request.values)
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    timeDifference = request.values.get("timeDifference")
    print(f"《app.py。开发维度》易bug table，前台传的参数startime={startTime}， endtime={endTime}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_easybug_table_fordrawmap_withdeveloper_orderby_date(startTime, endTime, timeDifference)
        print('《app.py。开发维度》一定时间颗粒度,易bug 产生比率曲线, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_easybug_table_fordrawmap_withdeveloper_orderby_date(startTime, endTime, timeDifference)
        print('《app.py。开发维度》一定时间颗粒度,易bug 产生比率曲线, 返回json==jsonStr=====', json_str)

    return json_str


# 10）开发维度，按时间（时间可自定义）统计bug解决的及时性考量：一二级bug一定时间内（可自定义）的解决率，三四级bug一定时间内（可自定义时间）
@app.route('/getBugSolveRateTableForDrawMapALongtimeWithDeveloper', methods=['POST', 'GET'])
def getBugSolveRateTableForDrawMapALongtimeWithDeveloper():
    # 获取前台传的参数
    print(request.values)
    startTime = request.values.get("startTime")
    endTime = request.values.get("endTime")
    timeDifference = request.values.get("timeDifference")
    print(f"《app.py。开发维度》一定时间颗粒度，bug解决率（12级 34级） table，前台传的参数startime={startTime}， endtime={endTime}")

    json_str = ''

    # 默认使用 get 请求
    if request.method == "GET":
        print('get请求')
        json_str = buglist.get_bugsolverate_table_fordrawmap_withdeveloper_orderby_date(startTime, endTime, timeDifference)
        print('《app.py。开发维度》一定时间颗粒度，bug解决率（12级 34级）, 返回json==jsonStr=====', json_str)

    if request.method == "POST":
        print('get请求')
        json_str = buglist.get_bugsolverate_table_fordrawmap_withdeveloper_orderby_date(startTime, endTime, timeDifference)
        print('《app.py。开发维度》一定时间颗粒度，bug解决率（12级 34级）, 返回json==jsonStr=====', json_str)

    return json_str


# #######  开发维度 end########################

# #########################  bug操作相关 end ############################################################################


# 主函数
if __name__ == '__main__':
    app.run(debug=True)
