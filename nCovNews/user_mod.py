import datetime
from nCovNews import db
from nCovNews import datatype

def post_word(id,word,replyto=0):
    session = db.session
    name = datatype.USER.query.filter_by(userid=id).first().name
    discuss = datatype.DISCUSS(userid=id,username=name,date=datetime.datetime.today(),word=word,likes=0,replyto=replyto)
    session.add(discuss)
    session.commit() # 修改数据库

def delete_all():
    session = db.session
    session.query(datatype.DISCUSS).delete()
    session.commit()


