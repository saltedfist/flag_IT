import time
from database.ext import DB
from sqlalchemy import Column, Integer, DateTime, String, INT
from sqlalchemy.dialects.mysql import TINYINT,VARCHAR,INTEGER
from api.utils.secret import render_password


# 签到
class Sign(DB.Model):
    __tablename__ = 'sign'
    # 此处缺少目标完成时间算出最大休假时间及最小休假时间
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  # 签到id
    uid = Column(Integer, primary_key=True, nullable=False)  # 用户id
    target_id = Column(Integer,primary_key=True, nullable=False) # 目标id
    target_name = Column(VARCHAR(255), nullable=False)# 目标标题
    number_of_days = Column(Integer, nullable=False)  # 目标完成天数
    create_time = Column(DateTime)  # 创建时间
    img = Column(VARCHAR(255))
    content = Column(VARCHAR(255))  # 备注

    # day_off = Column(VARCHAR(255), nullable=False)  # 休假时间
    # sign_time = Column(DateTime, nullable=False)# 签到时间
    # challenge_gold = Column(INT, default=0)  # 挑战金额(单位分)
    # insist_day = Column(INT)# 当前坚持天数
    # privacy = Column(INT)  # 是否公开,1公开,2隐私
    # modified_time = Column(DateTime)  # 修改时间
    # reminder_time = Column(DateTime)  # 提醒时间
    # pay_type = Column(VARCHAR(255))  # 支付类型
    # status = Column(TINYINT, default=1)  # 目标状态 0 正在进行,1 成功, 2 失败