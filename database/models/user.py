import time
from database.ext import DB
from sqlalchemy import Column, Integer, DateTime, String, INT
from sqlalchemy.dialects.mysql import TINYINT,VARCHAR,INTEGER
from api.utils.secret import render_password

# from utils.secret import render_password

ADMIN_USER_PERMISSION = 1
OPERATOR_USER_PERMISSION = 2
NONE_PERMISSION = 0


def current_datetime():
    return time.strftime('%y-%m-%d %H:%M:%S')

# 用户表
class User(DB.Model):
    __tablename__ = 'flag_user'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(30), unique=True)#用户名
    password = DB.Column(DB.String(64))  # 密码
    openid = DB.Column(DB.VARCHAR(255))# 后期接微信小程序会使用到 openid
    email = DB.Column(DB.VARCHAR(254))  # 邮箱
    phone = DB.Column(DB.String(30), default=None)#手机号
    integral = DB.Column(DB.Integer, default=0)# 积分 (平台内 代金币)
    money = DB.Column(DB.Integer, default=0)# rmb 用户金额
    permission = DB.Column(DB.INT, default=NONE_PERMISSION)#权限
    create_time = DB.Column(DB.DateTime)#创建时间
    update_time = DB.Column(DB.DateTime)# 更新时间
    status = DB.Column(DB.INT, default=0)# 状态：默认1：正常
    # icon = Column(String(256), default='')# 头像

    def __init__(self, **kwargs):
        for k in ['name', 'phone', 'permission', 'status', 'password', 'email']:
            v = kwargs.get(k)
            if v:
                setattr(self, k, v)
        self.password = render_password(kwargs.get('password'))
        self.create_time = current_datetime()

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
    def get_user_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def add_user(cls, kwargs):
        # kwargs['password'] = render_password(kwargs.get('password'))
        # kwargs['current_datetime'] = current_datetime()
        item = cls(**kwargs)
        try:
            DB.session.add(item)
            DB.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def check(cls, email, passwd):
        user = cls.get_user_by_email(email)
        if not user:
            return u'{0} is not exists or permission error.'.format(email)
        return user if user.password == render_password(passwd) else u'{0} is not exists or permission error.'.format(email)

    @classmethod
    def check_email(cls, email):
        user = cls.get_user_by_email(email)
        if not user:
            return u'{0} is not exists.'.format(email)
        else:
            return 0

    @classmethod
    def update_user(cls, uid, kwargs):
        try:
            DB.session.query(User).filter(
                User.id == uid
            ).update(kwargs)
            DB.session.commit()
            return True
        except Exception as e:
            print(e)
            return False