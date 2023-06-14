from pydantic import BaseModel


class UserAccessToken(BaseModel):
    """
    与AccessToken相关的用户信息
    """
    user_id: int  # 用户id
    phone: str  # 手机号
