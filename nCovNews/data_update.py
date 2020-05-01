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
        data_df.to_csv('nCovNews/data/data_all.csv' , index=False , encoding="utf_8_sig")
    except BaseException as err:
        print('error: report request fail!')
        return 1 # 错误代码1，请求失败
    except:
        return 2 # 错误代码2，未知异常
    else:
        return 0

def province_fix( data ):
    province_msg = pd.read_csv('nCovNews/data/province_msg.csv')
    f = province_msg.set_index('province')['province1'].to_dict()
    data['provinceCode'] = data['provinceCode'].apply(lambda x:f[x])
    return data

def getdata( date ):
    data_all = pd.read_csv('nCovNews/data/data_all.csv')
    # 填充空缺数据
    data = data_all.fillna('None')
    # 日期处理
    date_today = date.strftime('%Y-%m-%d')
    date_y = ( date + datetime.timedelta(days = -1) ).strftime('%Y-%m-%d')
    # 中国疫情报告生成
    data_t = data.loc[(data['date'] == date_today) & ((data['country'] == '中国') | (data['countryCode'] == '中国')) & (data['city'] == 'None')]
    data_y = data.loc[(data['date'] == date_y) & ((data['country'] == '中国') | (data['countryCode'] == '中国')) & (data['city'] == 'None')]
    data_y.index = data_t.index
    data_ch = data_t.copy()
    data_ch['adding'] = data_t['confirmed'] - data_y['confirmed'] # 计算新增
    data_ch = province_fix(data_ch) # 省份名修复
    data_ch = data_ch.nlargest( 100 ,'confirmed' ) # 按确诊数排序
    data_ch.to_csv('nCovNews/data/%s中国疫情报告.csv'%date_today , index=False , encoding="utf_8_sig",)
    return data

# date_today = datetime.datetime.today()
# date_yesterday = date_today + datetime.timedelta(days = -1)
# getdata(date_today)

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
        print('|>--------------------|0%',end='\r',flush = True)
        update_report()
        print('|==============>------|70%',end='\r',flush = True)
        get_news(1,10)
        print('|================>----|80%',end='\r',flush = True)
        get_information(1,10)
        print('|==================>--|90%',end='\r',flush = True)
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
    # 添加调度任务
    scheduler.add_job(update_all, 'interval', seconds=time)
    # 启动调度任务
    scheduler.start()



