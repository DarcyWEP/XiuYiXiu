#encoding: utf-8

# Power By Dazedark
# 用户信息的修改

from user.my import my
from send_email import sendMail
from flask import jsonify, request, session, Response
from models import *
from exts import db
import random
import string

@my.route('/alterUsername/', methods=['POST'])
def alterUsername():
    '''
        函数功能：修改用户名
        函数返回：return jsonify({'code': {flag} })  flag为1则修改成功，为2则用户不存在，为3则用户未登录
    '''
    userId = session.get('userId')
    newUsername = request.form.get('newUsername')
    if userId:  #用户已登录
        user = User.query.filter(User.id == userId).first()
        if user:  # 如果用户存在
            user.username = newUsername
            db.session.commit()
            return jsonify({'code' : 1})
        else:
            return jsonify({'code': 2})
    else:
        return jsonify({'code': 3})

@my.route('/sendAlterEmail/', methods=['POST'])
def sendAlterEmail():
    '''
        函数功能：发送修改邮箱的验证码（分批发送）
        函数返回：return jsonify({'code': {flag} })  flag为1则发送成功，为2则用户不存在，为3则用户未登录
    '''
    userId = session.get('userId')
    newEmail = request.form.get('newEmail')
    if userId:  # 用户已登录
        user = User.query.filter(User.id == userId).first()
        if user:  # 如果用户存在
            emailCode = EmailVerifyCode.query.filter(EmailVerifyCode.email == newEmail).first() #提取老验证码
            verifyCode = ''.join(random.sample(string.digits, 6))  # 生成一个随机的6位数验证码
            if emailCode: # 如果存在该邮箱未超时的话会发送与第一次请求相同的验证码(使用老邮箱来存储数据)
                if (datetime.now() - emailCode.createTime).seconds >= 1800:  # 验证码已超时，使用新的验证码
                    emailCode.verifyCode = verifyCode
                    emailCode.createTime = datetime.now()
                    db.session.commit() #存储本次验证码

                    leftVerifyCode = verifyCode[0:3]
                    rightVerifyCode = verifyCode[3:] #拆分验证码

                    print('leftVerifyCode = ', leftVerifyCode)
                    print('rightVerifyCode = ', rightVerifyCode)
                    content1 = "您正在修改咻一修的邮箱，，前三位验证码为【{code}】。" \
                               "后三位验证码已发送至老邮箱，请前往老邮箱获取。验证码30分钟内有效，如非本人操作，请忽略。".format(code=leftVerifyCode)
                    content2 = "您正在修改咻一修的邮箱，，后三位验证码为【{code}】。" \
                               "前三位验证码已发送至新邮箱，请前往新邮箱获取。验证码30分钟内有效，如非本人操作，请忽略。".format(code=rightVerifyCode)
                    sendMail(newEmail, content1)
                    sendMail(user.email, content2) #分别发送验证码
                    return jsonify({'code': 1})
                else: #验证码未超时
                    verifyCode = emailCode.verifyCode
                    leftVerifyCode = verifyCode[0:3]
                    rightVerifyCode = verifyCode[3:]  # 拆分验证码

                    print('leftVerifyCode = ', leftVerifyCode)
                    print('rightVerifyCode = ', rightVerifyCode)
                    content1 = "您正在修改咻一修的邮箱，，前三位验证码为【{code}】。" \
                               "后三位验证码已发送至老邮箱，请前往老邮箱获取。验证码30分钟内有效，如非本人操作，请忽略。".format(code=leftVerifyCode)
                    content2 = "您正在修改咻一修的邮箱，，后三位验证码为【{code}】。" \
                               "前三位验证码已发送至新邮箱，请前往新邮箱获取。验证码30分钟内有效，如非本人操作，请忽略。".format(code=rightVerifyCode)
                    sendMail(newEmail, content1)
                    sendMail(user.email, content2)  # 分别发送验证码
                    return jsonify({'code': 1})
            else:  # 不存在该邮箱，则添加到数据库
                newEmailVerifyCode = EmailVerifyCode(email=newEmail, verifyCode=verifyCode, createTime=datetime.now())
                db.session.add(newEmailVerifyCode)
                db.session.commit() # 添加一个新的验证码到数据库

                leftVerifyCode = verifyCode[0:3]
                rightVerifyCode = verifyCode[3:]  # 拆分验证码

                print('leftVerifyCode = ', leftVerifyCode)
                print('rightVerifyCode = ', rightVerifyCode)
                content1 = "您正在修改咻一修的邮箱，，前三位验证码为【{code}】。" \
                           "后三位验证码已发送至老邮箱，请前往老邮箱获取。验证码30分钟内有效，如非本人操作，请忽略。".format(code=leftVerifyCode)
                content2 = "您正在修改咻一修的邮箱，，后三位验证码为【{code}】。" \
                           "前三位验证码已发送至新邮箱，请前往新邮箱获取。验证码30分钟内有效，如非本人操作，请忽略。".format(code=rightVerifyCode)
                sendMail(newEmail, content1)
                sendMail(user.email, content2)  # 分别发送验证码
                return jsonify({'code': 1})
        else:
            return jsonify({'code': 2})
    else:
        return jsonify({'code': 3})


@my.route('/alterEmail/', methods=['POST'])
def alterEmail():
    '''
        函数功能：修改邮箱
        函数返回：return jsonify({'code': {flag} })  flag为1则修改成功，为2则验证码错误，为3则用户不存在，为4则用户未登录
    '''
    userId = session.get('userId')
    verifyCode = request.form.get('verifyCode')
    newEmail = request.form.get('newEmail')
    if userId:  #用户已登录
        user = User.query.filter(User.id == userId).first()
        if user:  # 如果用户存在
            oldEmailCode = EmailVerifyCode.query.filter(EmailVerifyCode.email == newEmail).first()  # 提取数据库的验证码
            if oldEmailCode and verifyCode == oldEmailCode.verifyCode: # 提交的验证码与数据库的验证码进行对比
                user.email = newEmail
                db.session.commit()
                db.session.delete(oldEmailCode)
                db.session.commit()
                return jsonify({'code': 1}) # 修改成功
            else:
                return jsonify({'code': 2}) # 验证码错误
        else:
            return jsonify({'code': 3}) # 用户不存在
    else:
        return jsonify({'code': 4}) # 用户未登录

# 以下是修改密码的三个接口

@my.route('/alterPassword/useOldPassword/', methods=['POST'])
def alterPassword():
    '''
         函数功能：使用原始密码来修改密码
        函数返回：return jsonify({'code': {flag} })  flag为1则修改成功，为2则原密码错误，为3则用户不存在，为4则用户未登录
    '''
    userId = session.get('userId')
    oldPassword = request.form.get('oldPassword')
    newPassword = request.form.get('newPassword')
    if userId:  # 用户已登录
        user = User.query.filter(User.id == userId).first()
        if user:  # 如果用户存在
            if user.verifyPassword(password=oldPassword): # 如果原始密码正确
                user.password(newPassword)
                db.session.commit()
                return jsonify({'code': 1})  # 修改成功
            else: #原始密码错误
                return jsonify({'code': 2})  # 原密码错误
        else:
            return jsonify({'code': 3})  # 用户不存在
    else:
        return jsonify({'code': 4})  # 用户未登录