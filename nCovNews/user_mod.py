import datetime
from nCovNews import db
from nCovNews import datatype

def post_word(name,word):
    session = db.session
    discuss = datatype.DISCUSS(name=name,date=datetime.datetime.today(),word=word)
    session.add(discuss)
    session.commit() # 修改数据库


