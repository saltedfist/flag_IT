import json
import time
from flask import request
from api import api
from api.utils.response import Error
from database.ext import redis_client
from database.models.api_docs import ApiDocs
from database.models.user import User


@api.route('/admin/api-add', methods=['POST'])
def api_add():
    error = Error(0, 'success')
    access_token = request.headers.get("Access-Token")
    uid = redis_client.get(access_token)
    if not uid:
        error.err_code = 9
        error.err_msg = 'access token 为空'
        return error.make_json_response()
    user = User.get_user_by_id(int(uid))
    if user.id != 1:
        error.err_code = 9
        error.err_msg = '该用户暂无此权限，请联系管理员。'
        return error.make_json_response()
    api_info = request.json if request.json else {}
    api_name = api_info.get('api_name')
    api_url = api_info.get('api_url')
    request_mothod = api_info.get('request_mothod')
    parameter = api_info.get('parameter')
    re_example = api_info.get('re_example')
    re_info = api_info.get('re_info')
    if not all([api_name, api_url, request_mothod, parameter, re_example, re_info]):
        error.err_code = 9
        error.err_msg = "数据不全，提交失败！"
        return error.make_json_response()
    kwargs = {
        'api_name': api_name,
        'api_url': api_url,
        'request_mothod': request_mothod,
        'parameter': json.dumps(parameter),
        're_example': re_example,
        're_info': json.dumps(re_info),
        'create_time': time.strftime('%y-%m-%d %H:%M:%S'),
        'modified_time': time.strftime('%y-%m-%d %H:%M:%S'),
        'status': 1
    }
    add_status = ApiDocs.add_apidocs(kwargs=kwargs)
    if add_status:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '存储文档失败。'
    return error.make_json_response()




@api.route('/admin/api-history', methods=['GET'])
def api_history():
    error = Error(0, 'success')
    access_token = request.headers.get("Access-Token")
    uid = redis_client.get(access_token)
    if not uid:
        error.err_msg = 9
        error.err_code = 'access token 为空'
        return error.make_json_response()
    user = User.get_user_by_id(int(uid))
    if user.id != 1:
        error.err_code = 9
        error.err_msg = '该用户暂无此权限，请联系管理员。'
        return error.make_json_response()
    docs_id = request.args.get('docs_id')
    if docs_id:
        docs_info = ApiDocs.get_docs_info(int(docs_id))
    else:
        docs_info = ApiDocs.get_docs_info()
    error.set_data(docs_info)
    return error.make_json_response()


@api.route('/admin/api-update', methods=['POST'])
def api_update():
    error = Error(0, 'success')
    access_token = request.headers.get("Access-Token")
    uid = redis_client.get(access_token)
    if not uid:
        error.err_msg = 9
        error.err_code = 'access token 为空'
        return error.make_json_response()
    user = User.get_user_by_id(int(uid))
    if user.id != 1:
        error.err_code = 9
        error.err_msg = '该用户暂无此权限，请联系管理员。'
        return error.make_json_response()
    update_info = request.json if request.json else None
    docs_id = update_info.get('docs_id')
    if docs_id is None:
        error.err_code = 9
        error.err_msg = '缺少参数。'
        return error.make_json_response()
    docs_id = update_info.pop("docs_id")
    parameter = json.dumps(update_info.get('parameter'))
    update_info['parameter'] = parameter
    re_info = json.dumps(update_info.get('re_info'))
    update_info['re_info'] = re_info
    update_status = ApiDocs.update_docs(docs_id, update_info)
    if update_status:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '更新失败，请重试。'
    return error.make_json_response()


@api.route('/admin/api-del', methods=['POST'])
def api_del():
    error = Error(0, 'success')
    access_token = request.headers.get("Access-Token")
    uid = redis_client.get(access_token)
    if not uid:
        error.err_msg = 9
        error.err_code = 'access token 为空'
        return error.make_json_response()
    user = User.get_user_by_id(int(uid))
    if user.id != 1:
        error.err_code = 9
        error.err_msg = '该用户暂无此权限，请联系管理员。'
        return error.make_json_response()
    del_info = request.json
    docs_id = del_info.get('id')
    update_info = {
        'status': 0
    }
    update_status = ApiDocs.update_docs(docs_id, update_info)
    if update_status:
        return error.make_json_response()
    error.err_code = 9
    error.err_msg = '删除失败，请重试。'
    return error.make_json_response()

