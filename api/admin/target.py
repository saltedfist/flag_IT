from api import api
from flask import request, jsonify
from api.utils.secret import create_veri, render_password
from api.utils.response import Error
from database.models.target import Target_Info
from database.models.timing_task import Timing_Task
from database.models.user import User
from  database.models.account import Account
from database.redis_ut.func import verify_token
from utils import tasks

from database.ext import redis_client

# 添加目标
@api.route('/target/add', methods=["POST"])
def target_add():
    error = Error(0, '建立目标成功')
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
    number_of_days = json_data.get('number_of_days')
    day_off = json_data.get('day_off')
    annotation = json_data.get('annotation') if json_data.get('annotation') else None
    challenge_gold = json_data.get('challenge_gold')
    insist_day = json_data.get('insist_day') if json_data.get('insist_day') else 0
    privacy = json_data.get('privacy') if json_data.get('privacy') else 1
    reminder_time = json_data.get('reminder_time')
    pay_type = json_data.get('pay_type')  # 付钱有另外的接口提供.
    gold_type = json_data.get('gold_type')
    start_time = json_data.get('start_time')
    if not all([number_of_days, day_off, challenge_gold, reminder_time, pay_type, gold_type]):
        error.err_code = 9
        error.err_msg = "提交数据缺失,请确认后重新提交."
        return error.make_json_response()

    # 缺少判断,之前是否存在未完成flag. 是否让用户有且仅能立一个flag的问题还需再讨论.
    target_data = {
        'target_name': target_name,
        'number_of_days': number_of_days,
        'day_off': day_off,
        'annotation': annotation,
        'challenge_gold': challenge_gold,
        'insist_day': insist_day,
        'privacy': privacy,
        'reminder_time': reminder_time,
        'pay_type': pay_type,
        'gold_type': gold_type,
        'start_time': start_time
    }
    task_data = {
        'uid': uid,
        'type': 1,
        'tk_time': reminder_time,
    }
    # tk_status = Timing_Task.add(task_data) # 将提示时间加入定时表.
    add_status = Target_Info.add(target_data)
    if add_status is True:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '建立目标失败,请重新提交.'
    return error.make_json_response()

# 查看历史目标
@api.route('/target/history', methods=['GET'])
def target_history():
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
    target_info = Target_Info.get_target_info_by_uid(uid)
    return target_info


# 设置是否公开
@api.route('/target/set-privacy', methods=['GET'])
def set_privacy():
    error = Error(0, 'success')
    token = request.headers.get("Access-Token")
    if not token:
        error.err_code = 9
        error.err_msg = "token is None"
        return error.make_json_response()
    uid = verify_token(token)
    if uid is None:
        error.err_code = 8
        error.err_msg = "token error"
        return error.make_json_response()
    target_id = int(request.args.get('target_id')) if request.args.get('target_id') else 0
    privacy_status = int(request.args.get('privacy_status')) if request.args.get('target_id') else 0
    if all([target_id, privacy_status]):
        error.err_code = 7
        error.err_msg = '参数缺失,提交失败!'
        return error.make_json_response()
    target = Target_Info.get_target_one_info(uid, target_id)
    if target is None:
        error.err_code = 6
        error.err_msg = '未找该flag,请确认后提交!'
        return error.make_json_response()

    update_data = {
        'privacy': privacy_status,
    }
    update_status = Target_Info.update_target(uid, target_id, update_data)
    if update_status:
        return error.make_json_response()
    else:
        error.err_code = 5
        error.err_msg = '提交失败,请重试!'
        return error.make_json_response()

# 是否开设修改休假时间(待讨论)


