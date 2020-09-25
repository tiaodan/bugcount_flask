import hashlib
import configparser
import json
import datetime
import pymysql
import os
import xlsxwriter
import time
import sys

# 初始化变量
# currentpath = os.path.abspath(__file__)
currentpath = os.path.dirname(__file__)
print('当前路径-///////开头', currentpath)
# rootdir = os.path.abspath(os.path.dirname(currentpath) + os.path.sep + '..') # 当前路径上一层
rootdir = os.path.dirname(os.path.dirname(__file__))  # 当前路径上一层
print('根目录-//////开头==', rootdir)

# 获取md5值
def get_md5(arg):

    # 1 创建md5对象
    obj_md5 = hashlib.md5()

    # 2. 必须生命encode ,md5编码啊格式
    obj_md5.update(arg.encode(encoding='utf-8'))
    print('传递参数为', arg)
    md5_result = obj_md5.hexdigest()
    print('md5码为', md5_result)
    #返回md5码
    return md5_result


# 相对路径读取配置文件中数据库 参数
def get_dbargs_from_config_byrelativepath(relativepath):
    print('前端 读取配置db内容,以 jsonStr 键值对格式 返回')

    #  实例化configParser对象
    config = configparser.ConfigParser()

    # -read读取ini文件
    # 因为app。py 已经设置所有资源文件从根目录读取，config的路径直接从根目录写，如果写。。/就报错了
        #因为打包读取不到配置文件，所以读取绝对路径
    # 项目路径
    # # root_dir = os.path.split(os.path.realpath(__file__))[0] # exe 生产C:\Users\admin\AppData\Local\Temp
    # root_dir = os.path.dirname(os.path.realpath(sys.argv[0])) #这个可以，直接就读出根目录来
    # # real_root_dir = root_dir[0:-3]
    # real_root_dir = root_dir
    # print(f'项目路径为=={root_dir}')
    # print(f'真实项目路径为=={real_root_dir}')
    # print(f'项目路径为 类型=={type(real_root_dir)}')
    # # config.ini文件路径
    # config_filepath = os.path.join(real_root_dir, 'conf\config.ini')
    # print(f'配置文件路径为=={config_filepath}')
    #
    # # config.read('../conf/config.ini', encoding='utf-8')  # 打包的时候需要这样配置，否则读取不到配置文件
    # config.read(config_filepath, encoding='utf-8')

    # config.read('conf/config.ini', encoding='utf-8')
    config.read(relativepath, encoding='utf-8')
    print('配置config  sessions', config.sections())

    config_dict = dict()
    if config.sections() is not None:
        print('读取到配置文件内容')
        config_dict['db_host'] = config.get('db', 'db_host')
        config_dict['db_user'] = config.get('db', 'db_user')
        config_dict['db_passwd'] = config.get('db', 'db_passwd')
        config_dict['db_dbname'] = config.get('db', 'db_dbname')
        print('db_host=', config_dict['db_host'])
        print('db_user=', config_dict['db_user'])
        print('db_passwd=', config_dict['db_passwd'])
        print('db_dbname=', config_dict['db_dbname'])

        # 测试是否能连上数据库
        try:
            conn = pymysql.connect(config_dict['db_host'], config_dict['db_user'], config_dict['db_passwd'], config_dict['db_dbname'])

        except:
            # conn.close()
            print('\033[1;31;40m')  # 下一目标输出背景为黑色，颜色红色高亮显示
            print('*' * 50)
            print('\033[7;31m 已有配置未能连接数据库，请查看数据库配置！\033[1;31;40m')  # 字体颜色红色反白处理
            print('\033[7;31m 建议：1. 后台输入 (mysql -h域名 -u用户名 -p密码 数据库名称 )查看是否可以连接数据库！\033[1;31;40m')  # 字体颜色红色反白处理
            print("\033[7;31m 2.如果第1步无法成功，只用用户名和密码登录，命令行输入mysql -uroot -psunkaisens (sunkaisens为数据库密码)尝试登录mysql\033[1;31;40m")  # 字体颜色红色反白处理
            print("\033[7;31m 3.如果第2步无法成功，进行数据库授权 grant all privileges on *.* to 'root'@'%' identified by 'sunkaisens'; 然后flush privileges\033[1;31;40m")  # 字体颜色红色反白处理
            print('\033[7;31m 4.如果第3步成功，进行数据库重启操作（一般linux和windows的数据库授权完了不需要重启，但是部分windows电脑授权完毕后需要重启mysql），详见用户手册\033[1;31;40m')  # 字体颜色红色反白处理
            print('*' * 50)
            print('\033[0m')


    return config_dict


# 绝对路径读取配置文件中数据库 参数
def get_dbargs_from_config_byabspath():
    print('前端 读取配置db内容,以 jsonStr 键值对格式 返回')

    #  实例化configParser对象
    config = configparser.ConfigParser()

    # -从根目录read读取配置文件
    # 项目路径
    # # root_dir = os.path.split(os.path.realpath(__file__))[0] # exe 生产C:\Users\admin\AppData\Local\Temp
    # root_dir = os.path.dirname(os.path.realpath(sys.argv[0])) #这个可以，直接就读出根目录来
    # # real_root_dir = root_dir[0:-3]
    # real_root_dir = root_dir
    # print(f'项目路径为=={root_dir}')
    # print(f'真实项目路径为=={real_root_dir}')
    # print(f'项目路径为 类型=={type(real_root_dir)}')
    # # config.ini文件路径
    # config_filepath = os.path.join(real_root_dir, 'conf\config.ini')
    # print(f'配置文件路径为=={config_filepath}')
    #
    # # config.read('../conf/config.ini', encoding='utf-8')  # 打包的时候需要这样配置，否则读取不到配置文件
    # config.read(config_filepath, encoding='utf-8')

    # currentpath = os.path.abspath(__file__)
    currentpath = os.path.dirname(__file__)
    print('当前路径（绝对方法///////////））', currentpath)
    # root_dir = os.path.abspath(os.path.dirname(currentpath) + os.path.sep + "..")
    root_dir = os.path.dirname(os.path.dirname(__file__))
    print('根目录(绝对方法/////////////) ===', root_dir)
    config_abspath = os.path.join(root_dir, 'conf\config.ini')
    print('配置文件绝对路径=', config_abspath)
    # 读取配置文件
    config.read(config_abspath, encoding='utf-8')
    print('配置config  sessions', config.sections())

    config_dict = dict()
    if config.sections() is not None:
        print('读取到的配置文件内容============')
        config_dict['db_host'] = config.get('db', 'db_host')
        config_dict['db_user'] = config.get('db', 'db_user')
        config_dict['db_passwd'] = config.get('db', 'db_passwd')
        config_dict['db_dbname'] = config.get('db', 'db_dbname')
        print('db_host=', config_dict['db_host'])
        print('db_user=', config_dict['db_user'])
        print('db_passwd=', config_dict['db_passwd'])
        print('db_dbname=', config_dict['db_dbname'])
        print('读取到的配置文件内容============')
        # 测试是否能连上数据库
        try:
            conn = pymysql.connect(config_dict['db_host'], config_dict['db_user'], config_dict['db_passwd'], config_dict['db_dbname'])

        except:
            # conn.close()
            print('\033[1;31;40m')  # 下一目标输出背景为黑色，颜色红色高亮显示
            print('*' * 50)
            print('\033[7;31m 已有配置未能连接数据库，请查看数据库配置！\033[1;31;40m')  # 字体颜色红色反白处理
            print('\033[7;31m 建议：1. 后台输入 (mysql -h域名 -u用户名 -p密码 数据库名称 )查看是否可以连接数据库！\033[1;31;40m')  # 字体颜色红色反白处理
            print("\033[7;31m 2.如果第1步无法成功，只用用户名和密码登录，命令行输入mysql -uroot -psunkaisens (sunkaisens为数据库密码)尝试登录mysql\033[1;31;40m")  # 字体颜色红色反白处理
            print("\033[7;31m 3.如果第2步无法成功，进行数据库授权 grant all privileges on *.* to 'root'@'%' identified by 'sunkaisens'; 然后flush privileges\033[1;31;40m")  # 字体颜色红色反白处理
            print('\033[7;31m 4.如果第3步成功，进行数据库重启操作（一般linux和windows的数据库授权完了不需要重启，但是部分windows电脑授权完毕后需要重启mysql），详见用户手册\033[1;31;40m')  # 字体颜色红色反白处理
            print('*' * 50)
            print('\033[0m')


    return config_dict


# 读取 所有 配置文件  键值对
def get_allargs_from_config():
    print('读取配置文件所有内容,以 dict 字典返回')
    # 默认定义数据
    code = 500  # 默认失败
    msg = '读取配置文件失败'
    count = 0  # 结果个数
    data = {}
    config_data_arr = []  # json data数据里填充的键值对

    #  实例化configParser对象
    config = configparser.ConfigParser()

    # -read读取ini文件
    config.read('conf/config.ini', encoding='utf-8')
    print('配置config  sessions', config.sections())

    config_dict = dict()
    if config.sections() is not None:
        print('读取到配置文件内容')
        config_dict['db_host'] = config.get('db', 'db_host')
        config_dict['db_user'] = config.get('db', 'db_user')
        config_dict['db_passwd'] = config.get('db', 'db_passwd')
        config_dict['db_dbname'] = config.get('db', 'db_dbname')
        config_dict['testlink_quick_link'] = config.get('quick_links', 'testlink_quick_link')
        config_dict['redmine_quick_link'] = config.get('quick_links', 'redmine_quick_link')
        config_dict['oa_quick_link'] = config.get('quick_links', 'oa_quick_link')
        config_dict['enterprise_email_quick_link'] = config.get('quick_links', 'enterprise_email_quick_link')

        #顺利读取完毕，默认读取成功
        code = 200
        msg = "配置文件读取成功"
        count = len(config_dict)
        config_data_arr.append(config_dict)

    for i in config_dict:
        print(i)

    #  返回json格式的数据
    data['code'] = code
    data['msg'] = msg
    data['count'] = count
    data['data'] = config_data_arr
    # 转化下查询结果为{},{},{}这种格式======================
    # print('<admin.py> 搜索用户方法 type(data)== ', type(data))
    # print('<admin.py> 搜索用户方法 type== ', data)
    # json.dumps()用于将dict类型的数据转成str .json.loads():用于将str类型的数据转成dict
    json_str = json.dumps(data, ensure_ascii=False)
    print('读取全部配置文件   -->jsonStr== ', json_str)

    return json_str


# 读取 所有 配置文件  键值对 -暂时没用这个方法
def get_allargs_from_config_nouse():
    print('读取配置文件所有内容,以list返回')
    #  实例化configParser对象
    config = configparser.ConfigParser()

    # -read读取ini文件
    config.read('../conf/config.ini', encoding='utf-8')

    # 首先得到配置文件的所有分组，然后根据分组逐一展示所有
    config_key_value_list = list()
    for sections in config.sections():
        for items in config.items(sections):
            print(items)
            config_key_value_list.append(items)

    print('读取配置文件所有内容, 返回类型==', type(config_key_value_list))
    return config_key_value_list


#  获取一段时间内的，一定颗粒度（时间差）的日期 集合list
#  获取的间隔是 ['2020-01-01', '2020-01-07', '2020-01-14'] 时间间隔是6的
#  date_diffrent_str 7的倍数
def get_bug_submit_date_list(starttime_str, endtime_str, date_diffrent_str):

    print('开始时间', starttime_str)
    start_time = datetime.datetime.strptime(starttime_str, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(endtime_str, '%Y-%m-%d')
    print('???????????????????????????????type date-dic==', type(date_diffrent_str))
    date_diffrent_int = int(date_diffrent_str)
    print('???????????????????????????????type date-dic==', date_diffrent_str)
    # delta = datetime.timedelta(days= time_diffrent_int -1) # 时间差 eg.2020-01-01 + 时间差 = 2020-01-07（一周的日期）

    datesub = (end_time - start_time).days +1  # 起始 终止时间相减
    print('时间间隔，=', datesub)

    fortimes = datesub // date_diffrent_int
    # print('循环了多少次', fortimes)

    # 取余>=0 endTime = endtime_x 都= endtime，如果mod >0 多算一段时间 mod=0 不用多算一段时间
    # if datesub % dateDiffrent = 0:
        # pass
    date_submit_date = list()
    date_submit_date.append(starttime_str)

    for i in range(0, fortimes):  # 包左不包右
        # 是起始时间就不 -1
        # 是终止时间就 替换从endtime_x
        # print(f'当前第{i}次循环')

        delta = datetime.timedelta(days=date_diffrent_int * (i + 1) - 1)
        bug_submit_time_str = datetime.datetime.strftime((start_time + delta), '%Y-%m-%d')
        date_submit_date.append(bug_submit_time_str)
        # print(date_submit_date)

    if datesub % date_diffrent_int >0:
        date_submit_date.append(endtime_str)

    print('这段时间内的时间应该是', date_submit_date)
    return date_submit_date  # list


#  获取一段时间内的，一定颗粒度（时间差）的日期 集合list
#  获取的间隔是 ['2020-01-01', '2020-01-08', '2020-01-15'] 时间间隔是6的，方便sql语句计算 >=time1 < tim2 ;>=time2 <time3
#  date_diffrent_str 7的倍数
def get_bug_submit_date_list_return_countsqltime(starttime_str, endtime_str, date_diffrent_str):

    print('开始时间', starttime_str)
    start_time = datetime.datetime.strptime(starttime_str, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(endtime_str, '%Y-%m-%d')
    print('???????????????????????????????type date-dic==', type(date_diffrent_str))
    date_diffrent_int = int(date_diffrent_str)
    print('???????????????????????????????type date-dic==', date_diffrent_str)
    # delta = datetime.timedelta(days= time_diffrent_int -1) # 时间差 eg.2020-01-01 + 时间差 = 2020-01-07（一周的日期）

    datesub = (end_time - start_time).days +1  # 起始 终止时间相减
    # print('时间间隔，=', datesub)

    fortimes = datesub // date_diffrent_int
    # print('循环了多少次', fortimes)

    # 取余>=0 endTime = endtime_x 都= endtime，如果mod >0 多算一段时间 mod=0 不用多算一段时间
    # if datesub % dateDiffrent = 0:
        # pass
    date_submit_date = list()
    date_submit_date.append(starttime_str)

    # endtime +1
    delta_oneday = datetime.timedelta(days=1)
    endtime_str = datetime.datetime.strftime((end_time + delta_oneday), '%Y-%m-%d')

    for i in range(0, fortimes):  # 包左不包右
        # 是起始时间就不 -1
        # 是终止时间就 替换从endtime_x
        # print(f'当前第{i}次循环')

        delta = datetime.timedelta(days=date_diffrent_int * (i + 1))
        bug_submit_time_str = datetime.datetime.strftime((start_time + delta), '%Y-%m-%d')
        date_submit_date.append(bug_submit_time_str)
        # print(date_submit_date)

    if datesub % date_diffrent_int > 0:
        date_submit_date.append(endtime_str)

    print('这段时间内的时间应该是', date_submit_date)
    return date_submit_date  # list



# 写入excel文件
"""
功能：写入excel文件
参数：path : excel文件的输出路径，结尾必须带上文件后缀,基于项目根目录的路径。如 根目录是“D:” excelrelapath = "test1.xlsx" ->最前面不用加\\
注意：1. excel文件名不存在会自动创建
     2. excel文件上级文件夹，如果不存在，不会自动创建
"""
def wirte_file(excelrelpath):
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
    # 关闭workbook
    book.close()


# 功能：判读是否是日期格式
# 参数：1.传入的字符串 2. 日期格式字符串，如："%Y-%m-%d" ?带秒的如何表示？ %H:%M:%M 格式不对!
def is_valid_date(str, dataformat="%Y-%m-%d"):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, dataformat)
    return True
  except:
    return False