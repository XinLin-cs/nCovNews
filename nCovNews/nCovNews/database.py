import time
import datetime
import json
import requests
import pandas as pd
import numpy as np


def update_all():
    url = 'http://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json'
    data = requests.get(url).json()
    # json获取数据帧
    data_df = pd.DataFrame(data)
    data_df.to_csv('nCovNews/data/data_all.csv' , encoding="utf_8_sig")

def get_df():
    data = pd.read_csv('nCovNews/data/data_all.csv')
    return data

def get_data(data_all , date):
    # 日期转字符串
    date = date.strftime('%Y-%m-%d')
    # 筛选数据
    data_today = data_all[data_all['date'] == date]
    # 显示前100降序排序
    data_show = data_today.nlargest( 100 , 'confirmed' )
    data_show.to_csv('nCovNews/data/show.csv' , encoding="utf_8_sig")

    return data_today

# Template
# update()
# data_all = get_df()
# date_today = datetime.date.today()
# get_data(data_all , date_today)
