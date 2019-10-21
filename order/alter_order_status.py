#encoding: utf-8

# Power By Dazedark And PopMa
# 订单状态的查询

from order import order
from flask import jsonify, request, session
from models import *
from decorators import login_required
from datetime import datetime
from send_email import sendMail
from send_phone_code import sendPhoneCode
# from .send_code_Ali import send_sms


@order.route('/engineerTakeOrder/', methods=['POST'])
def engineerTakeOrder():
    engineerId = session.get('userId')
    if engineerId:
        engineer = User.query.filter(User.id == engineerId).first()  # 查询出工程师
    else:
        return jsonify({'code': -1}) # 获取cookie失败

    orderId = request.form.get('orderId')
    print(orderId)
    print('engineer.phoneNumber = %s' % engineer.phoneNumber)
    if orderId and engineer.phoneNumber: # 参数正确
        order = Order.query.filter(Order.id == orderId).first()
        if order and order.status == 0: #库中有该订单
            # 给维修师发送邮件
            content = "你咻一修网接单成功，你接单的时间是【{orderTakeTime}】。接到订单的订单号为【{orderNumber}】，报修人姓名是【{repairManName}】，" \
                      "手机号为【{repairManPhone}】，机器的主要问题是【{problem}】，报修人地址是【{address}】，" \
                      "希望在【{freeTime}】期间进行维修，具体时间和维修地址可与报修人自行协商，".format(orderTakeTime=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                                                        orderNumber=order.orderNumber, repairManName=order.repairMan.name,
                                                                         repairManPhone=order.repairMan.phone, problem=order.problem.problem,
                                                                         address=order.problem.address, freeTime=order.problem.freeTime)
            resultEmail = sendMail(engineer.email, content)
            # 给顾客发送短信
            params = {
                'time': str(order.createTime),
                'engineer': str(engineer.username),
                'phonenumber': str(engineer.phoneNumber)
            }
            resulPhone = sendPhoneCode(phoneNumber=order.repairMan.phone, signName='咻一修', templateCode='SMS_103985015', params=params)

            if resultEmail and resulPhone:
                order.takeTime = datetime.now()
                # order.takeTime = str(datetime.now()).split('.')[0]
                order.status = 1
                order.engineerId = engineerId
                db.session.commit()
                return jsonify({'code': 1}) # 接单成功
            else:
                return jsonify({'code': 0})  # 接单失败
        else:
            return jsonify({'code': 2}) # 订单不存在或订单状态不正确
    else: # 参数错误
        return jsonify({'code': 3}) # 非法参数请求

@order.route('/engineerFinishOrder/', methods=['POST'])
def engineerFinishOrder():
    engineerId = session.get('userId')
    if engineerId:
        engineer = User.query.filter(User.id == engineerId).first()  # 查询出工程师
    else:
        return jsonify({'code': -1}) # 获取cookie失败

    orderId = request.form.get('orderId')
    if orderId and engineer.phoneNumber: # 参数正确
        order = Order.query.filter(Order.id == orderId).first()
        if order and order.status == 1:
            order.finishedTime = datetime.now()
            # order.takeTime = str(datetime.now()).split('.')[0]
            order.status = 2
            db.session.commit()
            return jsonify({'code': 1}) # 完成订单
        else:
            return jsonify({'code': 2}) # 订单不存在或订单状态不正确
    else:
        return jsonify({'code': 3}) # 非法参数请求

@order.route('/cancelOrder/', methods=['POST'])
def cancelOrder():
    phoneNumber = request.form.get('phoneNumber')
    phoneVerifyCode = request.form.get('phoneVerifyCode')
    orderId = request.form.get('orderId')
    if orderId and phoneNumber and phoneVerifyCode: # 参数正确
        oldVerifyCode = PhoneVerifyCode.query.filter(PhoneVerifyCode.phoneNumber == phoneNumber).first()
        if oldVerifyCode.phoneVerifyCode == phoneVerifyCode and (datetime.now()-oldVerifyCode.createTime).seconds<1800: #验证码正确
            # db.session.delete(oldPhoneVerifyCode)
            # db.session.commit() # 删除手机认证信息
            order = Order.query.filter(Order.id == orderId).first()
            if order and order.status == 0:
                order.status = -1
                db.session.commit()
                return jsonify({'code': 1}) #取消成功
            else:
                return jsonify({'code': 2}) # 订单不存在或订单状态不正确
        else:
            return jsonify({'code': 3}) # 验证码错误
    else:
        return jsonify({'code': 4}) # 非法参数请求
