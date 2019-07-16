import time
from database.ext import DB
from sqlalchemy import Column, Integer, DateTime, String, INT
from sqlalchemy.dialects.mysql import TINYINT,VARCHAR,INTEGER
from api.utils.secret import render_password


# 签到
from database.models.api_docs import current_datetime


class Sign(DB.Model):
    __tablename__ = 'flag_sign'
    # 此处缺少目标完成时间算出最大休假时间及最小休假时间
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, nullable=False)  # 签到id
    uid = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 用户id
    target_id = DB.Column(DB.Integer, primary_key=True, nullable=False) # 目标id
    target_name = DB.Column(DB.VARCHAR(255), nullable=False)# 目标标题
    # number_of_days = DB.Column(DB.Integer, nullable=False)  # 目标完成天数
    insist_day = DB.Column(DB.Intege)# 当前完成的天数
    create_time = DB.Column(DB.DateTime)  # 签到时间
    img = DB.Column(DB.TEXT) # 图片 各个图片以逗号隔开
    status = DB.Column(DB.TINYINT, default=1)  # 目标状态 1 正常签到, 2 休假
    content = DB.Column(DB.VARCHAR(255))  # 签到内容
    def __init__(self, **kwargs):
        for k in [
            'target_name', 'target_id', 'content', 'img', 'insist_day', 'status','uid'
        ]:
            v = kwargs.get(k)
            if v:
                setattr(self, k, v)
        self.create_time = current_datetime()
        self.status = 0

    @classmethod
    def add(cls, kwargs):
        item = cls(**kwargs)
        try:
            DB.session.add(item)
            DB.session.commit()
            return True
        except Exception as e:
            print(e)
            return False