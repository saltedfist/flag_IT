from flask import request

from api import api
from api.utils.response import Error
from database.models.comment import Comment
from database.models.user import User
from database.redis_ut.func import verify_token

# 互相评论接口
@api.route('/comment/add', methods=["POST"])
def comment_add():
    error = Error(0, '评论成功')
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
    sign_id = json_data.get('sign_id')
    by_uid = json_data.get('by_uid')
    comment_id = json_data.get('comment_id') if json_data.get('comment_id') else 0
    comment = json_data.get('comment')# 前端得传html格式,后端直接存储
    type = json_data.get('type') if json_data.get('type') else 1
    status = json_data.get('status') if json_data.get('status') else 1
    if not all([sign_id, by_uid, comment_id, comment,type]):
        error.err_code = 9
        error.err_msg = "提交数据缺失,请确认后重新提交."
        return error.make_json_response()
    comment_data = {
        'sign_id': sign_id,
        'by_uid': by_uid,
        'comment_id': comment_id,
        'comment': comment,
        'type': type,
        'status': status,
        'uid': uid
    }
    add_status = Comment.add(comment_data)
    if add_status is True:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '评论失败,请重新评论.'
    return error.make_json_response()

# 显示评论接口
@api.route('/comment/view', methods =['GET'])
def comment_view():
    pass