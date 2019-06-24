import time
from database.ext import DB
# from utils.secret import render_password

ADMIN_USER_PERMISSION = 1
OPERATOR_USER_PERMISSION = 2
NONE_PERMISSION = 0


def current_datetime():
    return time.strftime('%y-%m-%d %H:%M:%S')


class Account(DB.Model):
    __tablename__ = 'account'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(30), unique=True)#用户名
    phone = DB.Column(DB.String(30), default=None)#手机号
    passwd = DB.Column(DB.String(64))#密码
    permission = DB.Column(DB.INT, default=NONE_PERMISSION)#权限
    create_time = DB.Column(DB.DateTime)#创建时间
    status = DB.Column(DB.INT, default=0)#类型
    team = DB.Column(DB.String(32))#所属团队
    icon = DB.Column(DB.String(256))