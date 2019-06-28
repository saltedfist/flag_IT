from database.ext import DB


class Account(DB.Model):
    __tablename__ = 'account'
    uid = DB.Column(DB.Integer, primary_key=True, autoincrement=False)
