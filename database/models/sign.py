import time
from database.ext import DB
from sqlalchemy import Column, Integer, DateTime, String, INT
from sqlalchemy.dialects.mysql import TINYINT,VARCHAR,INTEGER
from api.utils.secret import render_password


# 签到
class Sign(DB.Model):
    __tablename__ = 'flag_sign'
    # 此处缺少目标完成时间算出最大休假时间及最小休假时间
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, nullable=False)  # 签到id
    uid = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 用户id
    target_id = DB.Column(DB.Integer, primary_key=True, nullable=False) # 目标id
    target_name = DB.Column(DB.VARCHAR(255), nullable=False)# 目标标题
    number_of_days = DB.Column(DB.Integer, nullable=False)  # 目标完成天数
    create_time = DB.Column(DB.DateTime)  # 签到时间
    img = DB.Column(DB.TEXT) # 图片 各个图片以逗号隔开
    status = DB.Column(DB.TINYINT, default=1)  # 目标状态 1 正常签到, 2 休假
    content = DB.Column(DB.VARCHAR(255))  # 签到内容