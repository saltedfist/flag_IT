from database.ext import DB




# 用户关注以及查看粉丝表
class Audience(DB.Model):
    __tablename__ = 'flag_audience'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    uid = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 关注者id
    by_uid = DB.Column(DB.Integer, primary_key=True, nullable=False)# 被关注者id
    status = DB.Column(DB.INT, default=1)  # 发起类型 0 取关,1 关注
    update_time = DB.Column(DB.DateTime)  # 修改时间
    create_time = DB.Column(DB.DateTime)  # 创建时间