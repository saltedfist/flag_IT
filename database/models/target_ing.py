import time
from database.ext import DB
from sqlalchemy import Column, Integer, DateTime, String, INT
from sqlalchemy.dialects.mysql import TINYINT,VARCHAR,INTEGER
from api.utils.secret import render_password


# 正在进行目标
class Target_Info(DB.Model):
    __tablename__ = 'target_ing'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)# 目标id