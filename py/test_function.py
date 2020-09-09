import configparser
from py import utils
import os

"""
测试相对路径读取配置文件，不好用，比如绝对路径，每次通过util调用相对路径，还得传路径参数
"""
if __name__ == '__main__':
    config = configparser.ConfigParser()
    # config.read('../conf/config.ini', encoding='utf-8')
    # utils.get_dbargs_from_config_byrelativepath("../conf/config.ini")
    utils.get_dbargs_from_config_byabspath()


