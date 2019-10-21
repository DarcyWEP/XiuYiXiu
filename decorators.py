#encoding: utf-8

#Power By Dazedark And PopMa
#装饰器

from functools import wraps
from flask import session
import json

# 登录限制的装饰器，用于判断用户是否登录
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)  #这个return不可以缺少
        else:  # 如果没有登录，跳转到登录页面
            return json.dumps({
                'status': 'no',
                'reason': '没有登录'
            })
    return wrapper