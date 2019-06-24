from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

import config

#redis缓存
redis_client = StrictRedis(db=config.REDIS_DB, host=config.REDIS_ADDR)

#flask-sqlalchemy,数据库引擎与flask app绑定，请求内有效，线程内无效
DB = SQLAlchemy()

def commit():
    DB.session.commit()

#sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine(config.SQLALCHEMY_DB_URI)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine, autoflush=True)