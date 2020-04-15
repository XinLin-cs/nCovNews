"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import nCovNews.views

from nCovNews import database as db
import datetime 
import pandas as pd

# db.update_all()
data_all = db.get_df()
date_today = datetime.date.today()
db.get_data(data_all , date_today)