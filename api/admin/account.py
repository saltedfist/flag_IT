from flask import request, jsonify

from api import api
from database.models.account import Account
# from utils.sms import send_register_sms

from database.ext import redis_client


@api.route('/account/log-in', methods=["GET", "POST"])
def account_login():
    name = request.form.get('name')
    password = request.form.get("password")
    if not name or not password:
        return jsonify({"error": 1, "msg": "用户名或密码为空"})

    if type(Account.check(name, password)) is str:
        return jsonify({"error": 1, "msg": "用户名或密码错误"})
    else:
        user = Account.get_user_by_name(name)
        if user.status == 0 or user.status == '0':
            return jsonify({"error": 2, "msg": "该用户未激活，请联系管理员"})
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        s = Serializer(b'flag_nb_no_1')
        token = s.dumps({'id': str(user.id)})
        redis_client.set(token, user.id,  ex=7*24*3600)
        user_id = user.id
        user_uniacs_list = Uniac.get_data_by_info(owner_id=int(user_id))
        # print(user_uniacs_list)
        return jsonify({"error": 0, "msg": "登陆成功", "token": str(token, 'utf-8'), 'user_uniacs_list': user_uniacs_list},)