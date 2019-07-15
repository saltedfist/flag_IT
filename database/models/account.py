from sqlalchemy import Column, Integer, VARCHAR

from database.ext import DB

# 用户详情
class Account(DB.Model):
    __tablename__ = 'flag_account'
    uid = DB.Column(DB.Integer, primary_key=True, autoincrement=False) # 用户id
    areastr = DB.Column(DB.VARCHAR(255), default=None)# 所在城市
    company = DB.Column(DB.VARCHAR(255), default=None)# 所在公司
    fansnum = Column(Integer, default=0)# 粉丝数量
    follownum = Column(Integer, default=0)# 关注数量
    job = DB.Column(DB.VARCHAR(255), default=None)# 职业
    school = DB.Column(DB.VARCHAR(255), default=None)# 学校
    selfdesc = DB.Column(DB.VARCHAR(255), default=None)# 对自己的评价
    username = DB.Column(DB.VARCHAR(255), default=None)# 用户名
    zanmun = Column(VARCHAR(255), default=0)# 受赞数量
    sex = DB.Column(DB.Integer, default=None)# 性别
    icon = DB.Column(DB.String(256), default='')# 头像

