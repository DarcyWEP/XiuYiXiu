#encoding: utf-8

# Power By Dazedark And PopMa
# 用户下单

from order import order
from flask import jsonify, request
from models import *
from exts import db
from datetime import datetime
from send_phone_code import sendPhoneVerifyCode
from send_email import sendMail

@order.route('/orderCreate/', methods=['POST'])
def orderCreate():
    '''
        函数功能：需要维修的用户下单
        函数返回：return jsonify({'code': {flag} })  flag为1：下单成功，2：验证码错误或超时，3：部分参数为空
    '''
    name = request.form.get('name')
    phoneNumber = request.form.get('phoneNumber')
    phoneVerifyCode = request.form.get('phoneVerifyCode')
    freeTime = request.form.get('freeTime')
    problem = request.form.get('problem')
    address = request.form.get('address')
    schoolCode = request.form.get('schoolCode')

    if name and phoneNumber and freeTime and problem and phoneVerifyCode and schoolCode and address: # 如果全部不为空
        oldPhoneVerifyCode = PhoneVerifyCode.query.filter(PhoneVerifyCode.phoneNumber == phoneNumber).first() #获取存库验证码
        oldRepairMan = NeedRepairMan.query.filter(NeedRepairMan.phone == phoneNumber).first()
        school = School.query.filter(School.schoolCode == str(schoolCode)).first()
        if oldPhoneVerifyCode.phoneVerifyCode == phoneVerifyCode and (datetime.now()-oldPhoneVerifyCode.createTime).seconds<1800: # 如果验证码正确且未超时
            # db.session.delete(oldPhoneVerifyCode)
            # db.session.commit() # 删除手机认证信息

            if oldRepairMan: #如果这个人之前申请过维修
                oldRepairMan.name = name
                oldRepairMan.schoolId = school.id
                db.session.commit()  # 报修人信息修改(基本上是一样的)
            else: #如果这个人之前未申请过维修
                oldRepairMan = NeedRepairMan(phone=phoneNumber, name=name,  schoolId=school.id)
                db.session.add(oldRepairMan)
                db.session.flush()  # 获取报修人的ID
                db.session.commit() # 报修人信息入库

            newRepairProblem = RepairProblem(problem=problem, freeTime=freeTime, address=address)
            db.session.add(newRepairProblem)
            db.session.flush()   # 获取这个问题的ID
            db.session.commit()  # 维修信息入库（机型与系统类型没有）

            orders = Order.query.all()
            orderLen1 = (len(orders) + 1) % 9999
            orderLen2 = "%04d" % orderLen1 # 生成订单后四位
            newOrder = Order(problemId=newRepairProblem.id, repairManId=oldRepairMan.id)
            newOrder.orderNumber =datetime.now().strftime('%H%M') + str(school.id) + datetime.now().date().strftime('%Y%m%d') + str(orderLen2) # 订单号
            db.session.add(newOrder)
            db.session.commit()  #订单信息入库
            content = "有人在咻一修网下单啦，快看下有没有适合自己的单喔！！！----来自咻一修网的垃圾邮件www.51xiuyixiu.com"
            users = User.query.all()
            for user in users:
                sendMail(user.email, content)
            return jsonify({'code': 1})  # 下单成功
        else:
            return jsonify({'code': 2})  # 验证码错误或超时
    else:
        return jsonify({'code': 3})  # 部分参数为空

@order.route('/sendPhoneCode/', methods=['POST'])
def sendPhoneCode():
    '''
        函数功能：发送手机验证码
        函数返回：return jsonify({'code': {flag} })  flag为1则发送成功，为2则发送失败
    '''
    phoneNumber = request.form.get('phoneNumber')  # 从前端获取手机号
    result = False
    if phoneNumber: #手机号不为空
        result = sendPhoneVerifyCode(phoneNumber=phoneNumber)
    if result:
        print('已经给{phone}发送验证码!'.format(phone=phoneNumber))
        return jsonify({'code': 1})  # 发送成功
    else:
        return jsonify({'code': 2})  # 发送失败