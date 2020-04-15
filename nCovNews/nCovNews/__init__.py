"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import nCovNews.views


import datetime 
import pandas as pd

from nCovNews import database as db
# db.update_all() # 从github上同步数据，频繁调用会被ban
data_all = db.get_df() # 从数据库内读取数据表
date_today = datetime.date.today()
db.get_data(data_all , date_today) # 据日期获得筛选后的数据表