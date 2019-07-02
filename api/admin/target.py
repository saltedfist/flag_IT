from api import api
from flask import request, jsonify
from api.utils.secret import create_veri, render_password
from api.utils.response import Error
from database.models.user import User
from  database.models.account import Account
from database.redis_ut.func import verify_token
from utils import tasks

from database.ext import redis_client

@api.route('/target/add',methods=["POST"])
def target_add():
    error = Error(0, 'success')
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




