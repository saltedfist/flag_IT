from database.ext import DB

# 积分(平台代币) 明细  重新设计
class Integral_Detail(DB.Model):
    __tablename__ = 'flag_integral_detail'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, nullable=False)  # 明细id
    uid = DB.Column(DB.Integer,nullable=False)  # 用户id
    integral = DB.Column(DB.Integer, default=0) # 积分
    type = DB.Column(DB.SMALLINT, nullable=False) # 类型 1:+ 2: - 1：默认收入，2：支出
    status = DB.Column(DB.SMALLINT, default=1)  # 状态1：正常2：删除
    target_id = DB.Column(DB.Integer,default=0) # 目标id 注:目标可以为空,为空的情况是用户用积分兑换rmb
    create_time = DB.Column(DB.DateTime)  # 明细生成时间时间
    update_time = DB.Column(DB.DateTime)  # 更新时间
    source_info = DB.Column(DB.SMALLINT, default=0) # 明细说明

    @classmethod
    def add_integral_detail(cls, kwargs):
        item = cls(**kwargs)
        try:
            DB.session.add(item)
            DB.session.commit()
            return True
        except Exception as e:
            print('添加积分明细错误，%s' % e)
            return False