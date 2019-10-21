#encoding: utf-8

# Power By Dazedark
# 给用户的手机发送验证码
"""
    短信产品-发送短信接口
    Created on 2018-03-20
"""

'''
    阿里云短信python3
'''
import Ali_SMS_From_CSDN
import json
from models import *
from exts import db
import random
import string

def sendPhoneCode(phoneNumber, signName, templateCode, params):
    sms = Ali_SMS_From_CSDN.AliyunSMS()
    return  sms.send_single(phone=phoneNumber, sign=signName, template=templateCode, params=params)


def sendPhoneVerifyCode(phoneNumber):
    print('phoneNumber = %s' % phoneNumber)
    verifyCode = ''.join(random.sample(string.digits, 6))  # 生成一个随机的6位数验证码
    oldPhoneNumber = PhoneVerifyCode.query.filter(PhoneVerifyCode.phoneNumber == phoneNumber).first()  # 从数据库查找该邮箱是不是有之前的验证码而未注册
    # 数据库中的验证码在使用之后会删除，如果原来的验证码存在数据库中则有可能是因为超时，或者是拿过验证码但没有使用的情况
    if oldPhoneNumber:  # 如果存在该验证码未超时的话会发送与第一次请求相同的验证码
        if (datetime.now() - oldPhoneNumber.createTime).seconds >= 1800:  # 验证码已超时，使用新的验证码
            oldPhoneNumber.phoneVerifyCode = verifyCode
            oldPhoneNumber.createTime = datetime.now()
            db.session.commit()
            params = {
                'code': verifyCode
            }
            result = sendPhoneCode(phoneNumber=str(phoneNumber), signName=str('***'), templateCode=str('***'), params=params)
        else:
            params = {
                'code': oldPhoneNumber.phoneVerifyCode
            }
            result = sendPhoneCode(phoneNumber=str(phoneNumber), signName=str('***'), templateCode=str('***'), params=params)
    else:  # 不存在该该手机，则添加到数据库
        newPhoneVerifyCode = PhoneVerifyCode(phoneNumber=phoneNumber, phoneVerifyCode=verifyCode, createTime=datetime.now())
        db.session.add(newPhoneVerifyCode)
        db.session.commit()
        params = {
            'code': verifyCode
        }
        result = sendPhoneCode(phoneNumber=str(phoneNumber), signName=str('***'), templateCode=str('***'), params=params)
    return result










'''
    以下注释部分是腾讯云的发送短信的代码
'''
# from qcloudsms_py import SmsSingleSender
# from qcloudsms_py.httpclient import HTTPError
#
# appId = "1400076170"
# appKey = "3cc45795ddb5cc0fca87e3bd57d78fe7"
# ssender = SmsSingleSender(appId, appKey)
# def sendPhoneCode():
#     params = ["123455", "30"]
#     try:
#         result = ssender.send_with_param(86, "18775069116", "96902", params)
#     except HTTPError as e:
#         print(e)
#     except Exception as e:
#         print(e)
#
#     print(result)
#
#
# if __name__ == '__main__':
#     sendPhoneCode()



'''
    以下注释部分是阿里云python2.7的发送短信的代码（3以上的已经弃用）
'''
# from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
# from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
# from aliyunsdkcore.client import AcsClient
# import uuid
#
# REGION = "cn-hangzhou"# 暂时不支持多region
# # ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
# ACCESS_KEY_ID = "LTAI7adLLtMKuciT"
# ACCESS_KEY_SECRET = "fT4MhSaeLhMkeSp6ytuno10bSstYhc"
# acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
# # 请参考本文档步骤2
# # __business_id = uuid.uuid1()
# # business_id=__business_id
#
# def send_sms(phoneNumber, signName, templateCode, templateParam=None):
#     businessId = uuid.uuid1()
#     smsRequest = SendSmsRequest.SendSmsRequest()
#     # 申请的短信模板编码,必填
#     smsRequest.set_TemplateCode(templateCode)
#     # 短信模板变量参数,友情提示:如果JSON中需要带换行符,请参照标准的JSON协议对换行符的要求,比如短信内容中包含\r\n的情况在JSON中需要表示成\\r\\n,否则会导致JSON在服务端解析失败
#     if template_param is not None:
#         smsRequest.set_TemplateParam(templateParam)
#     # 设置业务请求流水号，必填。
#     smsRequest.set_OutId(businessId)
#     # 短信签名
#     smsRequest.set_SignName(signName);
#     # 短信发送的号码，必填。支持以逗号分隔的形式进行批量调用，批量上限为1000个手机号码,批量调用相对于单条调用及时性稍有延迟,验证码类型的短信推荐使用单条调用的方式
#     smsRequest.set_PhoneNumbers(phoneNumber)
#     # 发送请求
#     smsResponse = acs_client.do_action_with_exception(smsRequest)
#     return smsResponse

# __business_id = uuid.uuid1()
# print __business_id

# params = "{\"code\":\"12345\",\"product\":\"云通信\"}"
# print send_sms(__business_id, "1500000000", "云通信产品", "SMS_000000", params)
# if __name__ == '__main__':
#     phonenumber = '18775069116'
#     template_param = {'code':'2312'}
#     send_sms(phonenumber, '***', template_code='SMS_101125084', template_param=template_param)