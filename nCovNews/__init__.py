"""
The flask application package.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
# Flask-WTF配置
app.config['SECRET_KEY'] = 'hello-world-jcfuns' # CSRF保护密钥
# app.config['WTF_CSRF_ENABLED'] = False # 关闭CSRF保护
bootstrap=Bootstrap(app)
# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app

import nCovNews.views
