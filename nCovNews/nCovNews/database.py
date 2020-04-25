import time
import datetime
import json
import requests
import pandas as pd
import numpy as np

def update_report():
    # 从服务器获取数据
    url = 'https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json'
    try:
        data = requests.get(url).json()
        # json获取数据帧
        data_df = pd.DataFrame(data)
        # 保存至数据库
        data_df.to_csv('nCovNews/data/data_all.csv' , encoding="utf_8_sig")
    except BaseException as err:
        print('error: report request fail!')
        return 1 # 错误代码1，请求失败
    except:
        return 2 # 错误代码2，未知异常
    else:
        return 0

def get_df():
    # 更新数据库
    code = update_report()
    # 从数据库读取
    data = pd.read_csv('nCovNews/data/data_all.csv')
    return data

def findbydate(data_all , date='All' , country='All' , province='All', city='All'):
    # 筛选数据
    data = data_all.fillna('None')

    if (date != 'All'):
        # 日期转字符串
        date = date.strftime('%Y-%m-%d')
        data = data[data['date'] == date]
    if (country != 'All'):
        data = data[data['country'] == country]
    if (province != 'All'):
        data = data[data['province'] == province]
    if (city != 'All'):
        data = data[data['city'] == city]
    # 显示前100降序排序并导出
    msg = date + country + province + city
    data_show = data.nlargest( 100 , 'confirmed' )
    data_show.to_csv('nCovNews/data/%s.csv'%msg , encoding="utf_8_sig")
    return data

def get_news( page , num ):
    url = 'http://lab.isaaclin.cn/nCoV/api/news?page=%d&num=%d' % ( page , num )
    try:
        data = requests.get(url).json()
        time.sleep(1)
        data = data['results']
        data_df = pd.DataFrame(data)
        # 保存至数据库
        data_df.to_csv('nCovNews/data/news.csv' , encoding="utf_8_sig")
    except BaseException as err:
        print('error: news request fail!')
        return 1 # 错误代码1，请求失败
    except:
        return 2 # 错误代码2，未知异常
    else:
        return 0

def get_fakenews( page , num ):
    url = 'http://lab.isaaclin.cn/nCoV/api/rumors?page=%d&num=%d&rumorType=%d' % ( page , num , 0 )
    try:
        data = requests.get(url).json()
        time.sleep(1)
        data = data['results']
        data_df = pd.DataFrame(data)
        # 保存至数据库
        data_df.to_csv('nCovNews/data/fakenews.csv' , encoding="utf_8_sig")
    except BaseException as err:
        print('error: fakenews request fail!')
        return 1 # 错误代码1，请求失败
    except:
        return 2 # 错误代码2，未知异常
    else:
        return 0

def get_information( page , num ):
    url = 'http://lab.isaaclin.cn/nCoV/api/rumors?page=%d&num=%d&rumorType=%d' % ( page , num , 1 )
    try:
        data = requests.get(url).json()
        time.sleep(1)
        data = data['results']
        data_df = pd.DataFrame(data)
        # 保存至数据库
        data_df.to_csv('nCovNews/data/information.csv' , encoding="utf_8_sig")
    except BaseException as err:
        print('error: information request fail!')
        return 1 # 错误代码1，请求失败
    except:
        return 2 # 错误代码2，未知异常
    else:
        return 0


from apscheduler.schedulers.background import BackgroundScheduler

def update_all():
    try:
        starttime = datetime.datetime.today()
        print(' * updating start!')
        print(' * start at %s' % ( starttime.isoformat(sep='/') ) )
        print('|>--------------------|0%')
        update_report()
        print('|==============>------|70%')
        get_news(1,10)
        print('|================>----|80%')
        get_information(1,10)
        print('|==================>--|90%')
        get_fakenews(1,10)
        print('|====================>|100%')
    except BaseException as err:
        print(err)
    except:
        pass
    else:
        pass
    finishtime = datetime.datetime.today()
    print(' * last for %d seconds' %  ( finishtime - starttime ).seconds )
    print(' * updating finished! ')

def auto_update(time):
    update_all()
    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()  
    # 添加调度任务,间隔时长为 2 秒
    scheduler.add_job(update_all, 'interval', seconds=time)
    # 启动调度任务
    scheduler.start()

# Template
# data_all = get_df() # 从数据库内读取数据表
# date = datetime.date.today()
# 据日期获得筛选后的数据表
# findbydate( data_all , date , 'All' , 'None' , 'None' ) 
# findbydate( data_all , date , '中国' , 'All' , 'None' ) 
# findbydate( data_all , 'All' , '中国' , 'None' , 'None' )
# findbydate( data_all , 'All' , '美国' , 'None' , 'None' ) 
# findbydate( data_all , 'All' , 'All' , '湖北省' , 'None' )



