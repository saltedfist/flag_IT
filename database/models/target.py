import time
from database.ext import DB
from sqlalchemy import Column, Integer, DateTime, String, INT
from sqlalchemy.dialects.mysql import TINYINT,VARCHAR,INTEGER
from api.utils.secret import render_password


#
class Target(DB.Model):
    __tablename__ = 'his_target'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)# 目标id
    uid = Column(Integer, primary_key=True, nullable=False)#用户id
    number_of_days = Column(Integer, nullable=False)  # 天数
    day_off = Column(VARCHAR(255), nullable=False)# 休息时间
    status = Column(TINYINT, default=1)# 目标状态
    annotation = Column(VARCHAR(255))# 备注
    challenge_gold = Column(INT, default=0)# 挑战金额(单位分)
    # insist_day = Column(INT)# 坚持时间
    privacy = Column(INT)# 是否公开,1公开,2隐私
    create_time = Column(DateTime)# 创建时间
    modified_time = Column(DateTime)# 修改时间
    reminder_time = Column(DateTime)  # 提醒时间
    tar_ing_id = Column(INT, default='')# 正在进行目标
    his_target_id = Column(INT, default='')# 历史目标id
    pay_type = Column(VARCHAR(255))# 支付类型
