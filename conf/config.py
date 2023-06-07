import json
import logging
import os
from logging.handlers import RotatingFileHandler

import pymysql as pymysql

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# 加载配置


def read_file(path, encoding='utf-8'):
    with open(path, mode='r', encoding=encoding) as f:
        return f.read()


def load_config():
    config_path = os.path.join(BASE_DIR, "conf/config.json")
    if not os.path.exists(config_path):
        raise Exception('配置文件不存在，请根据config-template.json模板创建config.json文件')
    config_str = read_file(config_path)  # 将json字符串反序列化为dict类型
    conf = json.loads(config_str)
    return conf


# 数据库连接
config = load_config()
if DEBUG:
    MYSQL_CONFIG = {
        "creator": pymysql,
        "maxconnections": 500,  # 连接池允许的最大连接数，0和None表示不限制连接数
        "blocking": True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        "maxusage": None,  # 一个链接最多被重复使用的次数，None表示无限制
        "host": config.get("mysql_host_debug"),
        "port": config.get("mysql_port_debug"),
        "user": config.get("mysql_user_debug"),
        "password": config.get("mysql_passwd_debug"),
        "database": config.get("mysql_db_debug"),
        "charset": config.get("mysql_charset_debug")
    }
else:
    MYSQL_CONFIG = {
        "creator": pymysql,  # 使用链接数据库的模块
        "maxconnections": 500,  # 连接池允许的最大连接数，0和None表示不限制连接数
        "blocking": True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        "maxusage": None,  # 一个链接最多被重复使用的次数，None表示无限制
        "host": config.get("mysql_host"),
        "port": config.get("mysql_port"),
        "user": config.get("mysql_user"),
        "password": config.get("mysql_passwd"),
        "database": config.get("mysql_db"),
        "charset": config.get("mysql_charset")
    }

# 日志配置

# 如果日志文件不存在，则创建
log_dir_path = os.path.join(BASE_DIR, "logs")
if not os.path.isdir(log_dir_path):
    os.makedirs(log_dir_path)

MAX_BYTES = 1024 * 1024 * 250  # 每个日志文件最大250M
BACKUP_COUNT = 4  # 最多4个日志文件

# 1.默认的logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关 CRITICAL > ERROR > WARNING > INFO > DEBUG

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

# 打印到文件
file_handler = RotatingFileHandler(filename=os.path.join(log_dir_path, "log.log"), mode="a",
                                   maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8")
file_handler.setLevel(logging.INFO)  # 输出到file的log等级的开关
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 打印到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
if DEBUG:
    logger.addHandler(console_handler)

if __name__ == '__main__':
    config = load_config()
    print(config)
