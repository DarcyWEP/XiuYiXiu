#encoding: utf-8

#Power By Dazedark And PopMa
#扩展，用来防止db与主app的循环调用(不知道是不是这样，记得不太清楚了)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
