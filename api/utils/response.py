from flask import jsonify
import json
from utils.jsond import JsonCustomEncoder
class Error:
    def __init__(self,err_code,err_msg):
        self.err_code = err_code
        self.err_msg = err_msg
        self.data = None

    def set_data(self, data):
        self.data = data

    def to_json(self, total_count=None, page_data=None):
        if total_count:
            return json.loads(
                json.dumps({"error": self.err_code, "msg": self.err_msg, "data": self.data, 'total_count': total_count},
                           cls=JsonCustomEncoder))
        if page_data:
            return json.loads(
                json.dumps({"error": self.err_code, "msg": self.err_msg, "data": self.data, 'page_data': page_data},
                           cls=JsonCustomEncoder))
        return json.loads(
            json.dumps({"error": self.err_code, "msg": self.err_msg, "data": self.data},
                       cls=JsonCustomEncoder))

    def make_json_response(self, total_count=None, page_data=None):
        if total_count:
            return jsonify(self.to_json(total_count))
        if page_data:
            return jsonify(self.to_json(page_data))
        return jsonify(self.to_json())