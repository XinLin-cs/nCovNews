import time
import datetime
import json
import requests
import pandas as pd
import numpy as np

def update_all():
    # 从服务器获取数据
    url = 'http://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json'
    try:
        data = requests.get(url).json()
        # json获取数据帧
        data_df = pd.DataFrame(data)
        # 保存至数据库
        data_df.to_csv('nCovNews/data/data_all.csv' , encoding="utf_8_sig")
    except BaseException as err:
        print(err)
        return 1 # 错误代码1，请求失败
    except:
        return 2 # 错误代码2，未知异常

    return 0

def get_df():
    # 更新数据库
    code = update_all()
    # 从数据库读取
    data = pd.read_csv('nCovNews/data/data_all.csv')
    return data

def findbydate(data_all , date='All' , country='All' , province='All', city='All'):
    # 筛选数据
    msg = ""
    data = data_all.fillna('None')

    if (date != 'All'):
        # 日期转字符串
        date = date.strftime('%Y-%m-%d')
        data = data[data['date'] == date]
        msg += date 
    if (country != 'All'):
        data = data[data['country'] == country]
        if (country != 'None'):
            msg += country 
    if (province != 'All'):
        data = data[data['province'] == province]
        if (province != 'None'):
            msg += province
    if (city != 'All'):
        data = data[data['city'] == city]
        if (city != 'None'):
            msg += city
    # 显示前100降序排序并导出
    if ( msg!='' ):
        data_show = data.nlargest( 100 , 'confirmed' )
        data_show.to_csv('nCovNews/data/%s.csv'%msg , encoding="utf_8_sig")
    return data

'''
# Template
data_all = get_df() # 从数据库内读取数据表
date = datetime.date.today()
# 据日期获得筛选后的数据表
findbydate( data_all , date , 'All' , 'None' , 'None' ) 
findbydate( data_all , 'All' , '中国' , 'None' , 'None' ) 
findbydate( data_all , 'All' , '美国' , 'None' , 'None' ) 
findbydate( data_all , 'All' , 'All' , '湖北省' , 'None' )
'''