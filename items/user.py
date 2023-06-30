from pydantic import BaseModel, validator


class UserAccessToken(BaseModel):
    """
    与AccessToken相关的用户信息
    """
    user_id: int  # 用户id
    phone: str  # 手机号

    @validator('phone')
    def validate_phone_number(cls, phone: str) -> str:
        phone = phone.strip()

        # 校验手机号长度
        if len(phone) != 11:
            raise ValueError('手机号长度不正确')

        # 校验手机号开头
        if not phone.startswith('1'):
            raise ValueError('手机号开头不正确')

        # 其他校验逻辑...

        return phone
