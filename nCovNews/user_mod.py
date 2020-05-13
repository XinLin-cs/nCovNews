import datetime
from nCovNews import db
from nCovNews import datatype

def post_word(word):
    session = db.session
    discuss = datatype.DISCUSS(name='jcdalao',date=datetime.datetime.today(),word=word)
    session.add(discuss)
    session.commit() # 修改数据库


