from database.ext import DB

# 目标
from database.models.api_docs import current_datetime
from database.models.integral_detail import Integral_Detail
from database.models.money_detail import Money_Detail
from database.models.user import User
from utils import timemac


class Target_Info(DB.Model):
    __tablename__ = 'flag_target_info'
    # 此处缺少目标完成时间算出最大休假时间及最小休假时间
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, nullable=False)  # 目标id
    uid = DB.Column(DB.Integer, primary_key=True, nullable=False)  # 用户id
    target_name = DB.Column(DB.VARCHAR(255), nullable=False)# 目标标题
    number_of_days = DB.Column(DB.Integer, nullable=False)  # 目标完成天数
    day_off = DB.Column(DB.Integer, nullable=False)  # 休假时间
    surplus_day_off = DB.Column(DB.Integer, nullable=False)  # 剩余休假时间
    # sign_time = Column(DateTime, nullable=False)# 签到时间
    annotation = DB.Column(DB.VARCHAR(255))  # 备注
    challenge_gold = DB.Column(DB.INT, default=0)  # 挑战金额（积分）  最低金额 100分，积分：100
    insist_day = DB.Column(DB.INT, default=0)# 当前坚持天数
    privacy = DB.Column(DB.INT)  # 是否公开,1公开,2隐私
    create_time = DB.Column(DB.DateTime)  # 创建时间
    modified_time = DB.Column(DB.DateTime)  # 修改时间
    reminder_time = DB.Column(DB.VARCHAR(30))  # 提醒时间
    pay_type = DB.Column(DB.VARCHAR(255))  # 支付类型 默认1：支付宝 2：微信 3：用户余额，4：积分
    status = DB.Column(DB.Integer, default=1)  # 目标状态 0 正在进行,1 成功, 2 失败
    gold_type = DB.Column(DB.Integer, default=1) #挑战金额类型默认1：金额   2：积分
    start_time = DB.Column(DB.DateTime) # 开始时间
    end_time = DB.Column(DB.DateTime) # 结束时间


    def __init__(self, **kwargs):
        for k in [
            'target_name', 'number_of_days', 'day_off', 'annotation', 'challenge_gold', 'insist_day', 'privacy', 'reminder_time', 'pay_type', 'gold_type'
        ]:
            v = kwargs.get(k)
            if v:
                setattr(self, k, v)
        self.create_time = current_datetime()
        self.status = 0


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
    def to_dict(self):
        data = self.__dict__
        data.pop('_sa_instance_state')
        return data

    @classmethod
    def get_target_info_by_uid(cls, uid: int):
        target_info = DB.session.query(cls).filter(cls.uid == uid).all()
        def merge_info_dict(item):
            item_dict = item.to_dict()
            return item_dict
        target_dict = (map(merge_info_dict, target_info))
        return target_dict

    @classmethod
    def change_target(cls, target_id: int, uid: int):

        target = DB.session.query(cls).filter(cls.target_id == target_id, cls.status == 0).one_or_none()
        if target.id != uid:
            return False
        challenge_gold = target.challenge_gold
        gold_type = target.gold_type
        target_id = target.id
        if target.insist_day + 1 >= target.number_of_days:
            target.status = 1
            target.end_time = timemac.today()
            DB.session.commit()
            # 挑战成功: 缺少给用户加金币,或者退还钱逻辑. 还需要在user表中 对积分或者rmb 进行修改.
            user = User.get_user_by_id(uid)
            user.update_time = timemac.today()
            if gold_type == 1: #1：金额   2：积分 待rmb与积分表建完,再完善逻辑.
                user.money = user.money + challenge_gold
                DB.session.commit()
                temp = {
                    'uid': user.id,
                    'money': user.money,
                    'type': 1,
                    'status': 1,
                    'target_id': target_id,
                    'create_time': timemac.today(),
                    'source_info': 1
                }
                add_status = Money_Detail.add_money_detail(temp)
                if add_status is False:
                    return False
                return True
            elif gold_type == 2:
                user.money = user.integral + target.challenge_gold
                DB.session.commit()
                temp = {
                    'uid': user.id,
                    'money': user.money,
                    'type': 1,
                    'status': 1,
                    'target_id': target_id,
                    'create_time': timemac.today(),
                    'source_info': 1
                }
                add_status = Integral_Detail.add_integral_detail(temp)
                if add_status is False:
                    return False
                return True
            else:
                return False
        else:
            target.insist_day = target.insist_day + 1
        DB.session.commint()
        return True

    @classmethod
    def update_target(cls, uid, target_id, kwargs):
        try:
            DB.session.query(Target_Info).filter(
                Target_Info.id == int(target_id)
                and Target_Info.admin_id == uid
            ).update(kwargs)
            DB.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    @classmethod
    def get_target_one_info(cls, uid, target_id):
        target_info = DB.session.query(cls).filter(cls.uid == uid, cls.id == target_id).one_or_none()
        return target_info