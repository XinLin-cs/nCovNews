"""
This script runs the nCovNews application using a development server.
"""
import time
from os import environ
from nCovNews import app
from nCovNews import db
from nCovNews import data_update

if __name__ == '__main__':
    # 实时数据更新
    db.drop_all()
    db.create_all()
    data_update.auto_update( 30*60 )
    # 启动服务器
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    time.sleep(2)
    app.run(HOST, PORT)
