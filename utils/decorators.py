"""
    装饰器函数
"""


import datetime
import functools
from typing import List, Dict, Union


def datetime_to_strftime(func):
    """
    datetime格式转str格式字符串，不转的话前端显示会带T："2023-06-09T16:02:26"
    示例：datetime.datetime(2023, 6, 9, 16, 2, 26)转为"2023-06-09 16:02:26"
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Union[List[Dict], Dict]:
        result: Union[List[Dict], Dict] = func(*args, **kwargs)

        is_dict_type = isinstance(result, Dict)

        if is_dict_type:
            results = [result]
        else:
            results = result

        for result in results:
            for key in ['create_time', 'update_time', 'publish_time', 'expire_time']:
                if key in result.keys():
                    result[key] = result[key].strftime('%Y-%m-%d %H:%M:%S')

        return results[0] if is_dict_type else results
    return wrapper


@datetime_to_strftime
def fun():
    ls = [{'create_time': datetime.datetime(2023, 6, 9, 16, 2, 26)}, ]
    return ls


def main():
    print(fun())


if __name__ == '__main__':
    main()
