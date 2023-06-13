"""
    自定义异常
"""
from typing import Any, Optional, Dict

from fastapi import HTTPException


class TaskCreateError(Exception):
    def __init__(self, message: str):
        self.message = message


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Optional[Dict[str, Any]] = None,
                 code: int = 0, msg: str = "", sub_code: int = 0, sub_msg: str = ""):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code
        self.msg = msg
        self.sub_code = sub_code
        self.sub_msg = sub_msg
