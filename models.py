# encoding: utf-8

# Power By Dazedark And PopMa
# 数据库模型
# 备注：模型名字首字母全部采用大写,数据库名采用下划线连接，其余变量采用首字母大写连接

from exts import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model): #网站维修师表
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True, index=True)
    passwordHash = db.Column(db.String(128), nullable=True)
    phoneNumber = db.Column(db.String(12), unique=True)
    authority = db.Column(db.Integer, default=0) # 权限：0-未认证 1-已认证
    teamId = db.Column(db.Integer, db.ForeignKey('teams.id'))
    schoolId = db.Column(db.Integer, db.ForeignKey('schools.id'))

    school = db.relationship('School', backref=db.backref('users'))
    team = db.relationship('Team', backref=db.backref('users'))

    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verifyPassword(self, password):
        return check_password_hash(self.passwordHash, password)

class Team(db.Model): #团队表
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teamName = db.Column(db.String(50), nullable=True, unique=True)
    introdution = db.Column(db.Text)
    peopleSum = db.Column(db.Integer)
    teamCode = db.Column(db.String(40), unique=True)  # 团队邀请码

class School(db.Model): #学校表
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    schoolName = db.Column(db.String(50), nullable=True, unique=True, index=True)
    schoolCode = db.Column(db.String(50), nullable=True, index=True)

class TeamLeader(db.Model):
    teamId = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True)
    schoolId = db.Column(db.Integer, db.ForeignKey('schools.id'))
    teamLeaderId = db.Column(db.Integer, db.ForeignKey('users.id'))

    school = db.relationship('School', backref=db.backref('teams'))


class Order(db.Model): # 订单
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderNumber = db.Column(db.String(50), nullable=True, unique=True, index=True)
    createTime = db.Column(db.DateTime, nullable=True, default=datetime.now)
    takeTime = db.Column(db.DateTime)  # 接单时间
    finishedTime = db.Column(db.DateTime)
    status = db.Column(db.Integer, nullable=True, default=0) #0：已下单 1：已接修 2：已完成
    repairManId = db.Column(db.Integer, db.ForeignKey('need_repair_mans.id'))
    engineerId = db.Column(db.Integer, db.ForeignKey('users.id'))
    problemId = db.Column(db.Integer, db.ForeignKey('repair_problems.id'))

    repairMan = db.relationship('NeedRepairMan', backref=db.backref('orders'))
    engineer = db.relationship('User', backref=db.backref('orders'))
    problem = db.relationship('RepairProblem', backref=db.backref('orders'))

class NeedRepairMan(db.Model): # 报修的人
    __tablename__ = 'need_repair_mans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(12), nullable=True, index=True, unique=True)
    name = db.Column(db.String(20), nullable=True)
    academy = db.Column(db.String(50)) # 学院
    schoolId = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True)

    school = db.relationship('School', backref=db.backref('RepairMans'))

class RepairProblem(db.Model): # 报修的问题
    __tablename__ = 'repair_problems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    problem = db.Column(db.String(100), nullable=True)
    machineType = db.Column(db.String(30))
    systemType  = db.Column(db.String(30))
    freeTime = db.Column(db.String(100),nullable=True)
    address = db.Column(db.String(150), nullable=True)

class Admin(db.Model): #管理员表
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    password = db.Column(db.String(128), nullable=True)
    joinTime = db.Column(db.DateTime, default=datetime.now, nullable=True)
    schoolId = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True)

    school = db.relationship('School', backref=db.backref('admins'))

# class

class EmailVerifyCode(db.Model):  #邮箱验证码
    __tablename__ = 'email_verify_codes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=True, index=True)
    verifyCode = db.Column(db.String(10), nullable=True)
    createTime = db.Column(db.DateTime, nullable=True)

class PhoneVerifyCode(db.Model):  #短信验证码
    __tablename__ = 'phone_verify_codes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phoneNumber = db.Column(db.String(12), nullable=True, index=True)
    phoneVerifyCode = db.Column(db.String(10), nullable=True)
    createTime = db.Column(db.DateTime, nullable=True)