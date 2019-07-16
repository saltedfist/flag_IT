from flask import request

from api import api
from api.utils.response import Error
from database.models.like import Like
from database.models.user import User
from database.redis_ut.func import verify_token

# 点赞接口
@api.route('/like/add', methods=["POST"])
def like_add():
    error = Error(0, '点赞成功')
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
    related_id = json_data.get('related_id')
    by_uid = json_data.get('by_uid')
    comment_id = json_data.get('comment_id') if json_data.get('comment_id') else 0
    type = json_data.get('type') if json_data.get('type') else 1
    status = json_data.get('status') if json_data.get('status') else 1
    if not all([related_id, by_uid, comment_id,type]):
        error.err_code = 9
        error.err_msg = "提交数据缺失,请确认后重新提交."
        return error.make_json_response()
    like_data = {
        'related_id': related_id,
        'by_uid': by_uid,
        'comment_id': comment_id,
        'type': type,
        'status': status,
        'uid': uid
    }
    add_status = Like.add(like_data)
    if add_status is True:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '点赞失败,请重新点赞.'
    return error.make_json_response()

# 查看点赞
@api.route('/like/view', methods= ['POST'])
def like_view():
    pass