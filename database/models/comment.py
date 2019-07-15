from database.ext import DB




# 评论回复表
class Comment(DB.Model):
    __tablename__ = 'comment'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)# 评论id
    sign_id = DB.Column(DB.String(30), default=None)  # 签到表ID
    uid = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 评论用户ID
    by_uid = DB.Column(DB.Integer, primary_key=True, nullable=False)# 被评论用户ID
    comment_id = DB.Column(DB.Integet)# 内容ID 默认0:直接评论
    comment = DB.Column(DB.TEXT) # html格式 评论的内容
    status = DB.Column(DB.Integer) # 状态默认1：正常，2：删除
    create_time = DB.Column(DB.DateTime)  # 创建时间
    type = DB.Column(DB.Integer) # 1,直接评论 2 评论 3 回复