from database.ext import DB
from database.models.api_docs import current_datetime


class Timing_Task(DB.Model):
    __tablename__ = 'flag_timing_task'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, nullable=False) # 定时任务id
    uid = DB.Column(DB.Integer, nullable=False)  # 用户id
    type = DB.Column(DB.Integer, nullable=False,) # 定时类型 1,提醒时间, 2,目标定时
    tk_time = DB.Column(DB.DateTime) # 执行的时间
    create_time = DB.Column(DB.DateTime) # 创建时间
    status = DB.Column(DB.Integer) # 定时状态 1 正常,0 取消


    def __init__(self, **kwargs):

        for k in [
            'uid', 'type', 'tk_time'
        ]:
            v = kwargs.get(k)
            if v:
                setattr(self, k, v)
        self.create_time = current_datetime()
        self.status = 1

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
