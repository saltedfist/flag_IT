from database.ext import DB





class Comment(DB.Model):
    __tablename__ = 'comment'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)# 评论id
    sign_id = DB.Column(DB.String(30), default=None)  # 签到id
    sponsor_id = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 发起者id
    by_sponsor_id = DB.Column(DB.Integer, primary_key=True, nullable=False) # 被发起者id
    create_time = DB.Column(DB.DateTime)  # 创建时间
    text = DB.Column(DB.VARCHAR(255))# 文字,表情评论(查看用户是否艾特关注用户)
    img = DB.Column(DB.VARCHAR(255))# 图片 # 前期先存入服务器(另外一台)
    status = DB.Column(DB.INT, default=1)  # 发起类型 0 删除,1,直接评论 2 评论 3 回复