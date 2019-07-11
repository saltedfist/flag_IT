from database.ext import DB





class Like(DB.Model):
    __tablename__ = 'like'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)  # 点赞id
    comment_id = DB.Column(DB.Integer,default=0)# 评论id
    sign_id = DB.Column(DB.Integer)# 签到id 如果评论id等于0,那就是用户给该条签到点赞.
    sponsor_id = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 发起者id
    by_sponsor_id = DB.Column(DB.Integer, primary_key=True, nullable=False) # 被发起者id
    create_time = DB.Column(DB.DateTime)  # 创建时间
    status = DB.Column(DB.INT, default=1)  # 发起类型 0 删除,1,直接点赞 2 点赞