from enum import Enum


class StatusCodeEnum(Enum):  # 错误码定义
    """ 状态码枚举类 """

    OK = (0, '成功')
    ERROR = (-1, '错误')

    USER_NOT_FOUND = (40001, '未找到用户')
    REQUEST_IS_TOO_FREQUENT = (40005, '请求过于频繁')

    ACCESS_TOKEN_HAS_EXPIRED = (40101, '访问令牌已过期')

    JSON_PARSE_ERR = (50001, 'JSON解析错误')

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def errmsg(self):
        """获取状态码信息"""
        return self.value[1]


# 任务状态
TASK_STATUS = {
    "waiting": 0,
    "doing": 1,
    "success": 2,
    "failed": 3,
}
