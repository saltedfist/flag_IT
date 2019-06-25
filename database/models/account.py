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
    email = DB.Column(DB.VARCHAR(254))#邮箱
    password = DB.Column(DB.String(64))#密码
    permission = DB.Column(DB.INT, default=NONE_PERMISSION)#权限
    create_time = DB.Column(DB.DateTime)#创建时间
    status = DB.Column(DB.INT, default=0)#类型
    icon = DB.Column(DB.String(256)) # 头像


    @classmethod
    def get_user_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def get_user_by_id(cls, uid):
        return cls.query.filter(cls.id == uid).first()

    @classmethod
    def get_user_by_phone(cls, phone):
        return cls.query.filter(cls.phone == phone).first()

    @classmethod
    def get_user_by_email(cls, phone):
        return cls.query.filter(cls.phone == phone).first()

    @classmethod
    def add_user(cls, kwargs):
        item = cls(**kwargs)
        try:
            DB.session.add(item)
            DB.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

