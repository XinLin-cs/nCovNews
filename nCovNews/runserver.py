"""
This script runs the nCovNews application using a development server.
"""

from os import environ
from nCovNews import app
from nCovNews import database as db

if __name__ == '__main__':
    # 实时数据更新
    db.auto_update( 20 )
    # 启动服务器
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
