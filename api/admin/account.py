from flask import request, jsonify
from api.utils.secret import create_veri
from api import api
from api.utils.response import Error
from database.models.account import Account
from utils import tasks

from database.ext import redis_client



# 注册
@api.route('/account/register', methods=["GET", "POST"])
def account_register():
    if request.method == 'POST':
        error = Error(0, '人生需要目标，有了目标才有奋斗的方向!')
        name = request.form.get('name')
        pass_word = request.form.get('password')
        phone = request.form.get('phone')
        email = request.form.get('email')
        verification = request.form.get('verification')  # 验证码
        if not (name and pass_word and phone and email and verification):
            error.err_code = 9
            error.err_msg = "参数为空"
            return error.make_json_response()
        check_name = Account.get_user_by_name(name)
        if check_name:
            error.err_code = 8
            error.err_msg = "该用户名已存在"
            return error.make_json_response()
        acc = {'name': name, 'password': pass_word, 'phone': phone, 'email': email}
        new_verification = redis_client.get(phone)
        if new_verification is None:
            error.err_code = 3
            error.err_msg = '请获取邮箱验证码'
            return error.make_json_response()
        if int(verification) != int(new_verification):
            error.err_code = 4
            error.err_msg = '该验证码错误，请尝试重新获取'
            return error.make_json_response()
        add_status = Account.add_user(acc)
        if add_status:
            return error.make_json_response()
        else:
            error.err_code = 5
            error.err_msg = "创建失败"
            return error.make_json_response()

# 发送邮箱
@api.route('/account/send-email', methods=["POST"])
def send_email():
    error = Error(0, 'success')
    info = request.json
    if info is None:
        error.err_code = '9',
        error.err_msg = '请填写邮箱'
    verification = create_veri()
    email = info.get('email')
    redis_client.set(email, verification, ex=900)
    msg = {
        's': "WelCome TO Join Us!",
        'r': email,
        'c': "[FLAG] 尊敬的用户:您的校验码:{0},工作人员不会索取,请勿泄露!".format(verification),
    }
    # 待开发
    tasks.send_mail(msg)

# 登陆
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

        # print(user_uniacs_list)
        pass