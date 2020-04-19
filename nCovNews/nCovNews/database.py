import time
import datetime
import json
import requests
import pandas as pd
import numpy as np

# Template
"""
data_all = get_df() # 从数据库内读取数据表
date = datetime.date.today()
findbydate( data_all , date ) # 据日期获得筛选后的数据表

"""

def update_all():
    # 从服务器获取数据
    url = 'http://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json'
    try:
        data = requests.get(url).json()
    except BaseException as err:
        return 1 # 错误代码1，请求失败
    except:
        return 2 # 错误代码2，未知异常

    # json获取数据帧
    data_df = pd.DataFrame(data)
    # 保存至数据库
    data_df.to_csv('nCovNews/data/data_all.csv' , encoding="utf_8_sig")
    return 0

def get_df():
    # 更新数据库
    code = update_all()
    # 从数据库读取
    data = pd.read_csv('nCovNews/data/data_all.csv')
    return data

def findbydate(data_all , date):
    # 日期转字符串
    date = date.strftime('%Y-%m-%d')
    # 筛选数据
    data = data_all[data_all['date'] == date]
    # 显示前100降序排序
    data_show = data.nlargest( 100 , 'confirmed' )
    # 导出数据
    data_show.to_csv('nCovNews/data/show.csv' , encoding="utf_8_sig")

    return data
