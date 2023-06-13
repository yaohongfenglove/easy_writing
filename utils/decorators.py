"""
    装饰器函数
"""


import datetime
import functools
from typing import List, Dict


def datetime_to_strftime(func):
    """
    datetime格式转str格式字符串，不转的话前端显示会带T："2023-06-09T16:02:26"
    示例：datetime.datetime(2023, 6, 9, 16, 2, 26)转为"2023-06-09 16:02:26"
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        results: List[Dict] = func(*args, **kwargs)
        for result in results:
            if 'create_time' in result.keys():
                result['create_time'] = result['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            if 'update_time' in result.keys():
                result['update_time'] = result['update_time'].strftime('%Y-%m-%d %H:%M:%S')
            if 'publish_time' in result.keys():
                result['publish_time'] = result['publish_time'].strftime('%Y-%m-%d %H:%M:%S')
        return results
    return wrapper


@datetime_to_strftime
def fun():
    ls = [{'create_time': datetime.datetime(2023, 6, 9, 16, 2, 26)}, ]
    return ls


def main():
    print(fun())


if __name__ == '__main__':
    main()
