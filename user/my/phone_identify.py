from user.my import my
from flask import jsonify, request, session
from models import *
from exts import db
from send_phone_code import sendPhoneVerifyCode
from send_email import sendMail

@my.route('/phoneIdentify/', methods=['POST'])
def phoneIdentify():
    '''
        函数功能：
        函数返回：
    '''
    userId = session.get('userId')
    if userId:
        user = User.query.filter(User.id == userId).first()
    else:
        return jsonify({'code': -1}) # 获取cookie失败
    phoneNumber = request.form.get('phoneNumber')
    verifyCode = request.form.get('verifyCode')
    if phoneNumber and verifyCode:
        oldVerifyCode = PhoneVerifyCode.query.filter(PhoneVerifyCode.phoneNumber == phoneNumber).first()
        if oldVerifyCode.phoneVerifyCode == verifyCode and (datetime.now()-oldVerifyCode.createTime).seconds<1800: # 如果验证码正确且未超时
            user.phoneNumber = phoneNumber
            db.session.commit()
            content = "你于北京时间{time}在咻一修网认证手机成功！".format(time=datetime.now())
            sendMail(user.email, content)
            return jsonify({'code': 1}) # 认证成功
        else:
            return jsonify({'code': 2}) # 验证码错误
    else:
        return jsonify({'code': 3}) # 非法参数请求

@my.route('/phoneIdentify/sendVerifyCode/', methods=['POST'])
def phoneIdentify_SendVerifyCode():
    phoneNumber = request.form.get('phoneNumber')
    oldPhone = User.query.filter(User.phoneNumber == phoneNumber).first()
    if oldPhone:
        return jsonify({'code': 0})  # 该手机已被使用
    result = False
    if phoneNumber:  # 手机号不为空
        result = sendPhoneVerifyCode(phoneNumber=phoneNumber)
    if result:
        print('已经给{phone}发送验证码!'.format(phone=phoneNumber))
        return jsonify({'code': 1})  # 发送成功
    else:
        return jsonify({'code': 2})  # 发送失败