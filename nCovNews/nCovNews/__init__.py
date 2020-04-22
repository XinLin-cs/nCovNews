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
db.findbydate( data_all , date , 'All' , 'None' , 'None' ) 
db.findbydate( data_all , 'All' , '中国' , 'None' , 'None' ) 
db.findbydate( data_all , 'All' , '美国' , 'None' , 'None' ) 
db.findbydate( data_all , 'All' , 'All' , '湖北省' , 'None' )
