"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
import os
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app

import nCovNews.views
