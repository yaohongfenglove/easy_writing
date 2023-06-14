"""
腾讯文档 https://cloud.tencent.com/document/product/382/55981
    pip install --upgrade tencentcloud-sdk-python
"""
import json
import traceback

from tencentcloud.common import credential
from tencentcloud.common.exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20210111 import sms_client, models

from conf.config import logger, config, DEBUG


def send_sms_verification_code(phone: str, verification_code: str, expire_minutes: int):
    """
    发送短信验证码
    :param phone: 收信人手机号
    :param verification_code: 验证码
    :param expire_minutes: 过期时间
    :return:
    """
    if DEBUG:
        return "123456"
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey，此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(config['tencent']['sms']['SECRET_ID'], config['tencent']['sms']['SECRET_KEY'])
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpprofile = HttpProfile()
        httpprofile.endpoint = "sms.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientprofile = ClientProfile()
        client = sms_client.SmsClient(cred, "ap-guangzhou", clientprofile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.SendSmsRequest()
        params = {
            "PhoneNumberSet": [f"+86{phone}"],
            "SmsSdkAppId": config['tencent']['sms']['SDK_APP_ID'],
            "SignName": config['tencent']['sms']['SIGN_NAME'],
            "TemplateId": config['tencent']['sms']['TEMPLATE_ID'],
            "TemplateParamSet": [f"{verification_code}", f"{expire_minutes}"]
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个SendSmsResponse的实例，与请求对象对应
        resp = client.SendSms(req)

        # 输出json格式的字符串回包
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        error_str = traceback.format_exc()
        logger.error(error_str)


def main():
    phone = "18649930703"
    verification_code = "123456"
    expire_minutes = config['tencent']['sms']['VERIFICATION_CODE_EXPIRE_MINUTES']
    resp = send_sms_verification_code(
        phone=phone,
        verification_code=verification_code,
        expire_minutes=expire_minutes
    )
    logger.info(resp)

    # 返回的json格式
    # {
    #     "SendStatusSet": [
    #         {
    #             "SerialNo": "3363:103203076016668620928241761",  # 发送流水号
    #             "PhoneNumber": "+8613413617619",  # 手机号码
    #             "Fee": 1,  # 计费条数
    #             "SessionContext": "",  # 用户session内容
    #             "Code": "Ok",  # 短信请求错误码
    #             "Message": "send success", # 短信请求错误码描述
    #             "IsoCode": "CN"  # 国家码或地区码
    #         }
    #     ],
    #     "RequestId": "42409463-5f65-4b44-ac9f-c2f0d0842c26"
    # }


if __name__ == '__main__':
    main()



