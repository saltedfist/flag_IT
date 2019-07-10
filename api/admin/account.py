from api import api
from flask import request, jsonify
from api.utils.secret import create_veri, render_password
from api.utils.response import Error
from database.models.user import User
from  database.models.account import Account
from utils import tasks

from database.ext import redis_client

# 注册
@api.route('/account/register', methods=["GET", "POST"])
def account_register():
    if request.method == 'POST':
        error = Error(0, '人生需要目标，有了目标才有奋斗的方向!')
        info = request.json
        if info is None:
            error.err_code = 9
            error.err_msg = "参数为空1"
            return error.make_json_response()
        name = info.get('name')
        pass_word = info.get('password')
        # phone = info.get('phone')
        email = info.get('email')
        # verification = request.form.get('verify')
        verification = info.get('verify')# 验证码
        if not (name and pass_word and email and verification):
            error.err_code = 9
            error.err_msg = "参数为空2"
            return error.make_json_response()
        check_name = User.get_user_by_name(name)
        if check_name:
            error.err_code = 8
            error.err_msg = "该用户名已存在"
            return error.make_json_response()
        acc = {'name': name, 'password': pass_word, 'email': email, 'status': 1}
        new_verification = redis_client.get(email)
        if new_verification is None:
            error.err_code = 3
            error.err_msg = '请获取邮箱验证码'
            return error.make_json_response()
        if str(verification) != str(new_verification, encoding='utf-8'):
            error.err_code = 4
            error.err_msg = '该验证码错误，请尝试重新获取'
            return error.make_json_response()
        add_status = User.add_user(acc)
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
        error.err_msg = '请填写邮箱信息'
    email = info.get('email')
    forget = info.get('forget')
    # verify_email = info.get('verify')
    # if verify_email:
    check_status = User.check_email(email)
    if type(check_status) is int and forget is None:
        error.err_code = 9
        error.err_msg = '该邮箱已注册过.'
        return error.make_json_response()
    elif type(check_status) is not int and forget:
        error.err_code = 9
        error.err_msg = '该邮箱未注册过,请注册后,登陆.'
        return error.make_json_response()
    verification = create_veri()
    # 限制用户发送邮件的次数。
    redis_client.set(email, verification)
    msg = {
        's': "WelCome TO Join Us!,啦啦啦~",
        'r': email,
        'c': "[FLAG]<br>尊敬的用户</br>您的校验码:{0}<br>工作人员不会索取,请勿泄露!</br>\n".format(verification),
        # 'c': verification
    }
    # 停止发送注册，直供开发人员使用
    # send_status = tasks.send_mail(msg)
    send_status = 2
    if send_status != 1:
        error.err_code = 9
        error.err_msg = '发送邮箱失败!'
        return error.make_json_response()
    else:
        return error.make_json_response()

# 登陆
@api.route('/account/login', methods=["POST"])
def account_login():
    if request.method == 'POST':
        json_info = request.json
        email = json_info.get('email')
        password = json_info.get("password")
        if not email or not password:
            return jsonify({"error": 1, "msg": "用户名或密码为空"})

        if type(User.check(email, password)) is str:
            return jsonify({"error": 1, "msg": "用户名或密码错误"})
        else:
            user = User.get_user_by_email(email)
            if user.status == 0 or user.status == '0':
                return jsonify({"error": 2, "msg": "该用户未激活，请联系管理员"})
            from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
            s = Serializer(b'flag_nb_no_1')
            token = s.dumps({'id': str(user.id)})
            redis_client.set(token, user.id,  ex=24*3600)
            return jsonify({"error": 0, "msg": "登陆成功", "token": str(token, 'utf-8')})


# 忘记密码
@api.route('/account/forget-passwd', methods = ["POST"])
def forget_passwd():
    error = Error(0, '人生需要目标，有了目标才有奋斗的方向!')
    forget_info = request.json
    email = forget_info.get('email')
    passwd = forget_info.get('password')
    verify = forget_info.get('verify')
    if not (email and verify):
        error.err_code = 9
        error.err_msg = "参数为空"
        return error.make_json_response()
    user = User.get_user_by_email(email)
    if user is None:
        error.err_code = 9
        error.err_msg = '该邮箱填写错误'
    new_veri_code = redis_client.get(email)
    if new_veri_code is None:
        error.err_code = 9
        error.err_msg = '请获取邮箱验证码'
        return error.make_json_response()
    if str(new_veri_code, encoding='utf-8') != str(verify):
        error.err_code = 9
        error.err_msg = '该验证码错误，请尝试重新获取'
        return error.make_json_response()
    passwd = render_password(passwd)
    acc = {
        'password': passwd
    }
    add_status = User.update_user(user.id, acc)
    if add_status:
        return error.make_json_response()
    else:
        error.err_code = 0
        error.err_msg = "修改成功"
        return error.make_json_response()