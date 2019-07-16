from database.ext import DB
from database.models.api_docs import current_datetime


class Like(DB.Model):
    __tablename__ = 'flag_like'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)  # 点赞id
    uid = DB.Column(DB.Integer)# 用户ID
    type = DB.Column(DB.Integer)# 类型：默认1：签到点赞  2：评论点赞
    related_id = DB.Column(DB.Integer,) #相关ID 根据类型来  签到表或者评论表中ID
    comment_id = DB.Column(DB.Integer, default=0)# 评论id
    create_time = DB.Column(DB.DateTime)  # 创建时间
    update_time = DB.Column(DB.DateTime) # 更新时间
    status = DB.Column(DB.INT, default=1)  # 状态：默认1；正常  2：取消

    def __init__(self, **kwargs):
        for k in [
            'related_id', 'by_uid', 'comment_id', 'type', 'status', 'uid'
        ]:
            v = kwargs.get(k)
            if v:
                setattr(self, k, v)
        self.create_time = current_datetime()

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