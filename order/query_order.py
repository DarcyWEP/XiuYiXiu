#encoding: utf-8

# Power By Dazedark And PopMa
# 订单状态的查询

from order import order
from flask import jsonify, request, session
from models import *
from sqlalchemy import and_
from datetime import datetime

from send_phone_code import sendPhoneVerifyCode

@order.route('/phoneQuery/', methods=['POST'])
def phoneQuery():
    phoneNumber = request.form.get('phoneNumber')
    phoneVerifyCode = request.form.get('phoneVerifyCode')
    page = request.form.get('page')

    print("phoneNumber = %s" % phoneNumber, "page = %s" % page, "phoneVerifyCode = %s" % phoneVerifyCode)
    if phoneNumber and page and phoneVerifyCode:
        oldPhoneVerifyCode = PhoneVerifyCode.query.filter(PhoneVerifyCode.phoneNumber == phoneNumber).first()  # 获取存库验证码
        if oldPhoneVerifyCode.phoneVerifyCode == phoneVerifyCode and (datetime.now()-oldPhoneVerifyCode.createTime).seconds<1800:
            # db.session.delete(oldPhoneVerifyCode)
            # db.session.commit() # 删除手机认证信息
            repairMan = NeedRepairMan.query.filter(NeedRepairMan.phone == phoneNumber).first() #提取需要维修人的信息
            if repairMan:
                orderLen = len(repairMan.orders)
                if orderLen > 0:
                    if (int(page) - 1) * 5 > orderLen:
                        return jsonify({'code': -1}) # 没有更多内容了
                    else:
                        repairMan.orders.reverse()
                        if (int(page)+1)*5 > orderLen:
                            orders = repairMan.orders[(int(page) - 1) * 5:]
                        else:
                            orders = repairMan.orders[(int(page) - 1) * 5:(int(page) * 5)]

                        ordersInfo = []
                        for order in orders: # 生成返回的订单信息
                            if order.status != 0 and order.status != -1: #工程师已经接单
                                orderInfo = {  # 单个订单信息（不返回用户的手机号和姓名，维修师接单时将发送给维修师）
                                    'orderId': order.id,
                                    'orderNumber': order.orderNumber,
                                    'createTime': str(order.createTime),
                                    'takeTime': str(order.takeTime),  # 维修师接修时间
                                    'finishedTime': str(order.finishedTime),
                                    'status': order.status,
                                    'engineerName': order.engineer.username,
                                    'engineerEmail': order.engineer.email,
                                    'problem': order.problem.problem,
                                    'machine': order.problem.machineType,
                                    'system': order.problem.systemType,
                                    'freeTime': order.problem.freeTime,
                                    'address': order.problem.address
                                }
                            else: # 工程师没有接单
                                orderInfo = {  # 单个订单信息（不返回用户的手机号和姓名，维修师接单时将发送给维修师）
                                    'orderId': order.id,
                                    'orderNumber': order.orderNumber,
                                    'createTime': str(order.createTime),
                                    'takeTime': str(order.takeTime),  # 维修师接修时间
                                    'finishedTime': str(order.finishedTime),
                                    'status': order.status,
                                    # 'engineerName': order.engineer.username,
                                    # 'engineerEmail': order.engineer.email,
                                    'problem': order.problem.problem,
                                    'machine': order.problem.machineType,
                                    'system': order.problem.systemType,
                                    'freeTime': order.problem.freeTime,
                                    'address': order.problem.address
                                }
                            ordersInfo.append(orderInfo)
                        msg = {
                            'currentPage': page,
                            'code': 1,  # 查询成功
                            'ordersInfo': ordersInfo,
                            'allPages': int((orderLen+4)/5),
                            'lastPage': True if orderLen - int(page) * 5 <= 0 else False# orderLen - int(page) * 5 <= 0 ? True : False
                        }
                        return jsonify(msg)
                else:
                    return jsonify({'code': 0}) # 没有订单
            else:
                return jsonify({'code': 0}) # 没有订单
        else:
            return jsonify({'code': 2}) # 验证码错误
    else:
        return jsonify({'code': 3}) # 部分空值

@order.route('/engineerQuery/', methods=['POST'])
def engineerQuery():
    engineerId = session.get('userId')
    # engineerId = int(request(request.form.get('engineerId'))) #测试用
    if engineerId:
        engineer = User.query.filter(User.id == engineerId).first()  # 查询出工程师
    else:
        return jsonify({'code': -1}) # 获取cookie失败
    status = request.form.get('status')
    page = int(request.form.get('page'))
    if status and page: # 参数不为空
        status = int(status)
        print( 'status = %s' % status)
        if status == 0:
            orders = Order.query.join(NeedRepairMan).filter(and_(NeedRepairMan.id == Order.repairManId, NeedRepairMan.schoolId == engineer.schoolId , # 层次查询
                                             Order.status == status)).paginate(page=page, per_page=5)
        elif status == 1:
            orders = Order.query.join(NeedRepairMan).filter(and_(NeedRepairMan.id == Order.repairManId, NeedRepairMan.schoolId == engineer.schoolId,  # 学校ID相等
                                                Order.status == status,
                                                Order.engineerId == engineerId) # 维修师ID相等
                                           ).order_by(Order.takeTime.desc()).paginate(page=page, per_page=5)
        elif status == 2:
            orders = Order.query.join(NeedRepairMan).filter(and_(NeedRepairMan.id == Order.repairManId, NeedRepairMan.schoolId == engineer.schoolId, # 学校ID相等
                                                Order.status == status,
                                                Order.engineerId == engineerId) # 维修师ID相等
                                           ).order_by(Order.finishedTime.desc()).paginate(page=page, per_page=5)
        else:
            return jsonify({'code': 0}) # 状态码出错
        print(orders)
        print(orders.pages)
        if orders.pages != 0:
            ordersInfo = []
            if status == 0: #订单未被维修师接修
                for order in orders.items:
                    orderInfo = {
                        'orderId': order.id,
                        'orderNumber': order.orderNumber,
                        'createTime': str(order.createTime),
                        'takeTime': str(order.takeTime),  # 维修师接修时间
                        'finishedTime': str(order.finishedTime),
                        'status': order.status,
                        # 'engineerName': order.engineer.username,
                        # 'engineerEmail': order.engineer.email,
                        'problem': order.problem.problem,
                        'machine': order.problem.machineType,
                        'system': order.problem.systemType,
                        'freeTime': order.problem.freeTime,
                        'address': order.problem.address
                    }
                    ordersInfo.append(orderInfo)
            else: #订单已被维修师接修
                for order in orders.items:
                    orderInfo = {
                        'orderId': order.id,
                        'orderNumber': order.orderNumber,
                        'createTime': str(order.createTime),
                        'takeTime': str(order.takeTime),  # 维修师接修时间
                        'finishedTime': str(order.finishedTime),
                        'status': order.status,
                        'engineerName': order.engineer.username,
                        'engineerEmail': order.engineer.email,
                        'problem': order.problem.problem,
                        'machine': order.problem.machineType,
                        'system': order.problem.systemType,
                        'freeTime': order.problem.freeTime,
                        'address': order.problem.address
                    }
                    ordersInfo.append(orderInfo)
            msg = {
                'code': 1, # 查询成功
                'currentPage': str(page),
                'ordersInfo': ordersInfo,
                'allPages': str(orders.pages),
                'lastPage': not (orders.has_next)
            }
            return jsonify(msg)
        else:
            return jsonify({'code': 2}) # 没有查询到匹配结果
    else:
        return jsonify({'code': 3}) # 部分参数为空
