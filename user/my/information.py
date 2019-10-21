#encoding: utf-8

# Power By Dazedark
# 用户信息的获取

from user.my import my
from flask import jsonify, request, session
from models import *
from exts import db

@my.route('/getInfo/', methods=['POST'])
def getInfo():
    '''
        函数功能：获取用户信息
        函数返回：return jsonify({'code': {flag} })  flag为1则请求成功并返回用户信息，为2则用户不存在，为3则用户未登录
    '''
    userId = session.get('userId')
    if userId:  #用户已登录
        user = User.query.filter(User.id == userId).first()
        if user:  # 如果用户存在
            if user.phoneNumber:
                msg = {
                    'code': 1,
                    'userInfo' : {
                        'username' : user.username,
                        'email': user.email,
                        'phone': user.phoneNumber[0:3]
                    }
                }
            else:
                msg = {
                    'code': 1,
                    'userInfo': {
                        'username': user.username,
                        'email': user.email,
                        'phone': None
                    }
                }
            return jsonify(msg)
        else:
            return jsonify({'code': 2})
    else:
        return jsonify({'code': 3})
    # email = request.form.get('email')
    # user = User.query.filter(User.email == email).first()
    # if user:  # 如果用户存在
    #     msg = {
    #         'code': 1,
    #         'userInfo' : {
    #             'username' : user.username,
    #             'email': user.email
    #         }
    #     }
    #     return jsonify(msg)

