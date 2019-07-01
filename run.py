import smtplib

from flask import Flask
from flask import redirect,request
import config
app = Flask(__name__)

@app.route('/')
def index():
    return"<h1>flag项目</h1><br/>" \
           "<h3>UI:贾钰.</h3><br/> "\
           "<h3>前端:王泽杰,汤礼坝.</h3><br/>" \
           "<h3>后端:叶佳,方东东.</h3><br/>" \
            "<h3>爬虫:陈善涛.<h3><br/>"\
"<h1>人生必须要有目标—计划决定人生 成就未来</h1>"


@app.errorhandler(404)
def not_found(error):
    return "<h1>页面不翼而飞啦~</h1>"


@app.errorhandler(500)
def internal_error(error):
    return "<h1>系统发脾气了~</h1>"


from database.ext import Mail
# Mail.init_app(app)
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'm13057785986@163.com'
app.config['MAIL_PASSWORD'] = 'a1b2c3'
# app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'm13057785986@163.com'
app.config['DEBUG'] = False
app.config['MAIL_USE_SSL'] = True
Mail.init_app(app)

#初始化数据库
with app.app_context():
    from database.models import *
    from database.ext import DB

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DB_URI
    app.config['HOSTNAME'] = config.HOSTNAME
    app.config['SECRET_KEY'] = config.SECRET_KEY
    DB.init_app(app)
    DB.create_all()


from api import api
app.register_blueprint(api, url_prefix="/api")



#运行，仅本地运行有效,正式环境下使用uwsgi代理
if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(host='0.0.0.0', port=5001)