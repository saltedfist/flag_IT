import json
import time

from sqlalchemy.orm.state import InstanceState
from database.ext import DB

ADMIN_USER_PERMISSION = 1
OPERATOR_USER_PERMISSION = 2
NONE_PERMISSION = 0


def current_datetime():
    return time.strftime('%y-%m-%d %H:%M:%S')


class ApiDocs(DB.Model):
    __tablename__ = 'api_docs'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    api_name = DB.Column(DB.VARCHAR(255), primary_key=True)  # 接口名
    api_url = DB.Column(DB.VARCHAR(255))  # 接口url
    request_mothod = DB.Column(DB.VARCHAR(255))  # 请求方式
    parameter = DB.Column(DB.VARCHAR(255))  # 参数
    re_example = DB.Column(DB.TEXT)  # 返回实例
    re_info = DB.Column(DB.VARCHAR(2048))  # 返回参数说明
    create_time = DB.Column(DB.DateTime)  # 创建时间
    modified_time = DB.Column(DB.DateTime)  # 修改时间
    status = DB.Column(DB.SMALLINT)  # 接口状态

    @classmethod
    def add_apidocs(cls, kwargs):
        item = cls(**kwargs)
        try:
            DB.session.add(item)
            DB.session.commit()
            return True
        except Exception as e:
            print('商品入库错误，%s' % e)
            return False

    @classmethod
    def get_docs_info(cls, docs_id=None):
        if docs_id:
            docs_list = DB.session.query(cls).filter(cls.status == 1, cls.id == docs_id).all()
        else:
            docs_list = DB.session.query(cls).filter(cls.status == 1).all()
        data_list = []
        for docs in docs_list:
            docs_info = {}
            docs_info["id"] = docs.id
            docs_info["api_name"] = docs.api_name
            docs_info["api_url"] = docs.api_url
            docs_info["request_mothod"] = docs.request_mothod
            docs_info["parameter"] = docs.parameter
            docs_info["re_example"] = json.dumps(docs.re_example)
            docs_info["re_info"] = docs.re_info
            docs_info["create_time"] = docs.create_time
            docs_info["modified_time"] = docs.modified_time
            docs_info["status"] = docs.status
            data_list.append(docs_info)
        return data_list

    @classmethod
    def update_docs(cls, docs_id, kwargs):
        try:
            DB.session.query(ApiDocs).filter(
                ApiDocs.id == int(docs_id)
            ).update(kwargs)
            DB.session.commit()
            return True
        except Exception as e:
            print(e)
            return False