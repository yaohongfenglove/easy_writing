from pydantic import BaseModel


class AccessTokenInfo(BaseModel):
    """
    访问令牌信息
    """
    user_id: int  # 用户id
    phone: str  # 手机号
