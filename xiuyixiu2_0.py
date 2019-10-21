#encoding: utf-8

#Power By Dazedark And PopMa
#主运行文件

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
import config
from exts import db
from models import *
from flask_cors import *
from user import user
from user.my import my
from datetime import timedelta
from order import order
from admin import admin

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
CORS(app, supports_credentials=True)

app.permanent_session_lifetime = timedelta(days=10)

app.register_blueprint(user, url_prefix='/user')  # 用户
app.register_blueprint(my, url_prefix='/user/my')  # 用户个人中心
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(admin, url_prefix='/admin')


# @app.route('/islogin')
# def my_context_processor():
#     print('is login')
#     user_id = session.get('user_id')
#     print(session)
#     if user_id:
#         user = User.query.filter(User.id == user_id).first()
#         return jsonify({
#             'status': 'ok',
#             'user': user.username,
#             'email': user.email,
#             'authority':user.authority
#         })
#     return jsonify({'status': 'no'})

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # app.run(port=8889, host='0.0.0.0', ssl_context=('./public.pem', './214356520920995.key'))
    app.run(port=8889, host='0.0.0.0')
