import json
import logging
import os
from logging.handlers import RotatingFileHandler

import pymysql as pymysql


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = True


def load_config():
    config_path = os.path.join(BASE_DIR, "conf/config.json")
    if not os.path.exists(config_path):
        raise Exception('配置文件不存在，请根据config-template.json模板创建config.json文件')

    with open(config_path, mode='r', encoding='utf-8') as f:
        config_str = f.read()
    conf = json.loads(config_str)  # 将json字符串反序列化为dict类型
    return conf


# 加载配置
config = load_config()


# 数据库连接
if DEBUG:
    MYSQL_CONFIG = {
        "creator": pymysql,
        "maxconnections": 500,  # 连接池允许的最大连接数，0和None表示不限制连接数
        "blocking": True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        "maxusage": None,  # 一个链接最多被重复使用的次数，None表示无限制
        "host": config["mysql"]["debug"]["host"],
        "port": config["mysql"]["debug"]["port"],
        "user": config["mysql"]["debug"]["user"],
        "password": config["mysql"]["debug"]["password"],
        "database": config["mysql"]["debug"]["database"],
        "charset": config["mysql"]["debug"]["charset"]
    }
else:
    MYSQL_CONFIG = {
        "creator": pymysql,  # 使用链接数据库的模块
        "maxconnections": 500,  # 连接池允许的最大连接数，0和None表示不限制连接数
        "blocking": True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        "maxusage": None,  # 一个链接最多被重复使用的次数，None表示无限制
        "host": config["mysql"]["production"]["host"],
        "port": config["mysql"]["production"]["port"],
        "user": config["mysql"]["production"]["user"],
        "password": config["mysql"]["production"]["password"],
        "database": config["mysql"]["production"]["database"],
        "charset": config["mysql"]["production"]["charset"]
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
