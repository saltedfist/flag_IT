from database.ext import DB




# 用户关注以及查看粉丝表
from database.models.api_docs import current_datetime


class Audience(DB.Model):
    __tablename__ = 'flag_audience'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    uid = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 关注者id
    by_uid = DB.Column(DB.Integer, primary_key=True, nullable=False)# 被关注者id
    status = DB.Column(DB.INT, default=1)  # 发起类型 0 取关,1 关注
    update_time = DB.Column(DB.DateTime)  # 修改时间
    create_time = DB.Column(DB.DateTime)  # 创建时间

    def __init__(self, **kwargs):
        for k in [
             'by_uid', 'status', 'uid'
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