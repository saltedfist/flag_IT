from flask import request

from api import api
from api.utils.response import Error
from database.models.audience import Audience
from database.models.comment import Comment
from database.models.user import User
from database.redis_ut.func import verify_token

# 添加关注用户
@api.route('/audience/add', methods=["POST"])
def audience_add():
    error = Error(0, '关注成功')
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
    by_uid = json_data.get('by_uid')
    status = json_data.get('status') if json_data.get('status') else 1
    if not all([by_uid]):
        error.err_code = 9
        error.err_msg = "提交数据缺失,请确认后重新提交."
        return error.make_json_response()
    audience_data = {
        'by_uid': by_uid,
        'status': status,
        'uid': uid
    }
    add_status = Audience.add(audience_data)
    if add_status is True:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '关注失败,请重新关注.'
    return error.make_json_response()

# 查看该用户关注,吸粉情况
@api.route('/audience/view-fans', methods=['GET'])
def view_fans():
    pass