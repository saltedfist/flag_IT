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


class User(DB.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)#用户名
    phone = Column(String(30), default=None)#手机号
    email = Column(VARCHAR(254))#邮箱
    password = Column(String(64))#密码
    permission = Column(INT, default=NONE_PERMISSION)#权限
    create_time = Column(DateTime)#创建时间
    status = Column(INT, default=0)#类型
    icon = Column(String(256)) # 头像


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
    @classmethod
    def check(cls, name, passwd):
        user = cls.get_user_by_name(name)
        if not user:
            return u'{0} is not exists or permission error.'.format(name)
        return user if user.passwd == render_password(passwd) else u'{0} is not exists or permission error.'.format(name)