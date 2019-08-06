from database.ext import DB

# rmb 明细  后期重新设计,持续用这张表会造成数据统计不完整性.
class Money_Detail(DB.Model):
    __tablename__ = 'flag_money_detail'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, nullable=False)  # 明细id
    uid = DB.Column(DB.Integer,nullable=False)  # 用户id
    money = DB.Column(DB.Integer, default=0) # rmb
    type = DB.Column(DB.SMALLINT, nullable=False) # 类型 1:+ 2:-
    status = DB.Column(DB.SMALLINT, default=1)  # 状态1：正常2：删除
    target_id = DB.Column(DB.Integer, default=0) # 目标id 注:目标可以为空,为空的情况是用户用积分兑换rmb
    create_time = DB.Column(DB.DateTime, default='')  # 明细生成时间时间
    update_time = DB.Column(DB.DateTime, default='')  # 更新时间
    source_info = DB.Column(DB.SMALLINT, default=0) # 明细说明 1 来自目标, 2 充值 3 兑换平台积分

    @classmethod
    def add_money_detail(cls, kwargs):
        item = cls(**kwargs)
        try:
            DB.session.add(item)
            DB.session.commit()
            return True
        except Exception as e:
            print('添加rmb明细错误，%s' % e)
            return False