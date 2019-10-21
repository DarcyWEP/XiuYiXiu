#encoding: utf-8

#Power By Dazedark And PopMa
#配置文件

#使用session必须要用到SECRET_KEY
#import os
#SECRET_KEY = os.urandom(24) #urandom随机生成一个24位的字符串
SECRET_KEY = 'fwp4RzMsoJPqiukyFnVWrg0C'
DEBUG = True

# 数据库配置：dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'          # 或pymysql
USERNAME = 'root'
PASSWORD = '******'
HOST = '127.0.0.1'          # 本地测试HOST
PORT = '3306'
DATABASE = 'xiuyixiu2_0'    # 事先创建好的数据库
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False      #禁止一个基本问题的报错
