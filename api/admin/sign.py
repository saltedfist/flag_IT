from flask import request
from api import api
from api.utils.response import Error
from database.models.target import Target_Info
from database.models.user import User
from database.models.sign import Sign
from database.redis_ut.func import verify_token


# 签到只有添加功能,业务逻辑已开发.(未测试)
@api.route('/sign/add', methods=["POST"])
def sign_add():
    error = Error(0, '签到成功')
    token = request.headers.get("Access-Token")
    if not token:
        error.err_code = 9
        error.err_msg = "token is None"
        return error.make_json_response()
    uid = verify_token(token)
    if uid is None:
        error.err_code = 9
        error.err_msg = "token error"
        return error.make_json_response()
    user = User.get_user_by_id(uid)
    if user is None:
        error.err_code = 9
        error.err_msg = "登陆时间已过期,请重启登陆"
        return error.make_json_response()
    json_data = request.json
    target_name = json_data.get('target_name') if json_data.get('target_name') else None
    target_id = json_data.get('target_id')
    content = json_data.get('content') if json_data.get('content') else None
    img = request.files.get('img')
    insist_day = json_data.get('insist_day') if json_data.get('insist_day') else 0
    status = json_data.get('status') if json_data.get('status') else 1
    if not all([target_id, img]):
        error.err_code = 9
        error.err_msg = "提交数据缺失,请确认后重新提交."
        return error.make_json_response()
    target = Target_Info.change_target(target_id, uid)
    if target is False:
        error.err_code = 9
        error.err_msg = '提交参数错误!,请确认后重新提交!'
        return error.make_json_response()

    sign_data = {
        'target_name': target_name,
        'target_id': target_id,
        'content': content,
        'img': img,
        'insist_day': insist_day,
        'status': status,
        'uid': uid
    }
    add_status = Sign.add(sign_data)

    if add_status is True:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '签到失败,请重新提交!'
    return error.make_json_response()