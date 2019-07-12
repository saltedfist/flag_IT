from sqlalchemy import Column, Integer, VARCHAR

from database.ext import DB

# 用户详情
class Account(DB.Model):
    __tablename__ = 'account'
    uid = Column(Integer, primary_key=True, autoincrement=False) # 用户id
    areastr = Column(VARCHAR(255), default=None)# 所在城市
    company = Column(VARCHAR(255), default=None)# 所在公司
    # fansnum = Column(Integer, default=0)# 粉丝数量
    # follownum = Column(Integer, default=0)# 关注数量
    job = Column(VARCHAR(255), default=None)# 职业
    school = Column(VARCHAR(255), default=None)# 学校
    selfdesc = Column(VARCHAR(255), default=None)# 对自己的评价
    username = Column(VARCHAR(255), default=None)# 用户名
    # zanmun = Column(VARCHAR(255), default=0)# 受赞数量
    sex = Column(Integer, default=None)# 性别
    # icon = Column(String(256), default='')# 头像
