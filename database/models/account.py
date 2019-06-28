from sqlalchemy import Column, Integer

from database.ext import DB


class Account(DB.Model):
    __tablename__ = 'account'
    uid = Column(Integer, primary_key=True, autoincrement=False)
