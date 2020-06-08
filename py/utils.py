import hashlib
import configparser


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


# 读取配置文件中数据库  参数
def get_dbargs_from_config():
    print('读取配置db内容,以 dict 字典 返回')
    #  实例化configParser对象
    config = configparser.ConfigParser()

    # -read读取ini文件
    # 因为app。py 已经设置所有资源文件从根目录读取，config的路径直接从根目录写，如果写。。/就报错了
    config.read('conf/config.ini', encoding='utf-8')
    print('配置config  sessions', config.sections())

    config_dict = dict()
    if config.sections() is not None:
        print('未读取到配置文件内容')
        config_dict['db_host'] = config.get('db', 'db_host')
        config_dict['db_user'] = config.get('db', 'db_user')
        config_dict['db_passwd'] = config.get('db', 'db_passwd')
        config_dict['db_dbname'] = config.get('db', 'db_dbname')
        print('db_host=', config_dict['db_host'])
        print('db_user=', config_dict['db_user'])
        print('db_passwd=', config_dict['db_passwd'])
        print('db_dbname=', config_dict['db_dbname'])

    return config_dict


# 读取 所有 配置文件  键值对
def get_allargs_from_config():
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


