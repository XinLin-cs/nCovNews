import datetime
from nCovNews import db
from nCovNews import datatype

def post_word(user,word,replyto=0):
    session = db.session
    discuss = datatype.DISCUSS(userid=user.userid,username=user.name,userphoto=user.photo,date=datetime.datetime.today(),word=word,likes=0,replyto=replyto)
    session.add(discuss)
    session.commit() # 修改数据库

def delete_all():
    session = db.session
    session.query(datatype.DISCUSS).delete()
    session.commit()


