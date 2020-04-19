"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import nCovNews.views


import datetime 
import pandas as pd

from nCovNews import database as db
data_all = db.get_df() # 从数据库内读取数据表
date = datetime.date.today()
data = db.findbydate( data_all , date ) # 据日期获得筛选后的数据表