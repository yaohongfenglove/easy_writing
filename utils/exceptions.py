"""
    自定义异常
"""


class TaskCreateError(Exception):
    def __init__(self, message: str):
        self.message = message
