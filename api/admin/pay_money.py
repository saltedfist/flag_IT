from flask import jsonify

from api import api


# 付钱,及充值 在这实现
# 测试付钱接口
@api.route('/pay-money', methods=["POST"])
def pay_money():
    return jsonify({"pay_type": 1, "gold_type": 1, "challenge_gold": 100})