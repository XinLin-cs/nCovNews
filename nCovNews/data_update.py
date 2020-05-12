import time
import datetime
import json
import requests
import pandas as pd
import numpy as np

from nCovNews import db
from nCovNews import datatype

def getdata_api():
    url = 'https://i.snssdk.com/forum/ncov_data/?data_type=%5B2%2C4%2C8%5D'
    html = requests.get(url).json()
    # print(html.keys())
    # dict_keys(['message', 'ncov_city_data', 'ncov_nation_data', 'map_config', 'city_code', 'treating_data', 
    # 'overseas_data', 'country_data', 'province_data', 'policy_data', 'focus_city_data'])

    # 国内数据
    nation = html['ncov_nation_data']
    nation = json.loads(nation)
    # print(nation_data.keys())
    # dict_keys(['updateTime', 'confirmedDate', 'suspectedDate', 'provinces', 'nationwide', 'world', 
    # 'nationwideIncr', 'nationTotal', 'confirmedIncrProvinceTop10', 'confirmedIncrProvinceTop10Text', 
    # 'nationLocalIncrText', 'incrTips', 'asymptomaticTitle', 'asymptomaticNumProvinceTop10', 
    # 'asymptomaticNumProvinceTop10Text', 'asymptomaticIncrProvinceTop10', 'asymptomaticIncrProvinceTop10Text', 
    # 'displayAsymptomatic'])

    updateTime = nation['updateTime']

    # 测试
    db.drop_all()
    db.create_all()
    session = db.session

    # 省份数据
    provinces = nation['provinces']
    # print(provinces[0].keys())
    # dict_keys(['id', 'name', 'confirmedNum', 'curesNum', 'deathsNum', 'treatingNum', 'treatingNumStr', 
    # 'asymptomaticNum', 'cities', 'series', 'updateTime', 'updateDate', 'confirmedIncr', 'provinceIncr', 
    # 'asymptomaticIncr', 'isTreatingNumClear'])
    for data in provinces:
        date = datetime.date.today()
        name = data['name']
        confirmed = data['confirmedNum']
        cures = data['curesNum']
        deaths = data['deathsNum']
        asymptomatic = data['asymptomaticNum']
        province = datatype.PROVINCE(date=date,name=name,confirmed=confirmed,cures=cures,deaths=deaths,asymptomatic=asymptomatic)
        session.add(province)

    # 中国总数据
    nationwide = nation['nationwide']
    # print(nationwide[0].keys())
    # dict_keys(['date', 'confirmedNum', 'suspectedNum', 'curesNum', 'deathsNum', 'suspectedIncr', 'curesRatio', 
    # 'deathsRatio', 'suspectedNumStr', 'suspectedIncrStr', 'treatingNum', 'inboundNum', 'inboundIncr',
    #  'asymptomaticNum', 'asymptomaticIncr'])
    for data in nationwide:
        date = pd.to_datetime(data['date'])
        confirmed = data['confirmedNum']
        suspected = data['suspectedNum']
        cures = data['curesNum']
        deaths = data['deathsNum']
        asymptomatic = data['asymptomaticNum']
        chinatotal = datatype.CHINATOTAL(date=date,confirmed=confirmed,suspected=suspected,cures=cures,deaths=deaths,asymptomatic=asymptomatic)
        session.add(chinatotal)

    # 海外数据
    overseas = html['overseas_data']
    overseas = json.loads(overseas)
    # print(overseas.keys())
    # dict_keys(['updateTime', 'country', 'total', 'incr', 'series', 'confirmedIncrTop10', 
    # 'confirmedIncrTop10Text', 'testingInfo', 'continent', 'confirmedIncr7DTop10', 'confirmedIncr7DTop10Text'])

    # 各国数据
    country = overseas['country']
    # print(country[0].keys())
    # dict_keys(['id', 'code', 'name', 'nationalFlag', 'countryTotal', 'countryIncr', 'series', 'provinces', 
    # 'isTreatingNumClear', 'confirmedPerMil', 'continent', 'updateTime'])
    for data in country:
        date = datetime.date.today()
        name = data['name']
        continent =data['continent']
        countryTotal = data['countryTotal']
        # print(countryTotal.keys())
        # dict_keys(['confirmedTotal', 'suspectedTotal', 'curesTotal', 'deathsTotal', 'treatingTotal',
        #  'inboundTotal', 'asymptomaticTotal'])
        confirmed = countryTotal['confirmedTotal']
        cures = countryTotal['curesTotal']
        deaths = countryTotal['deathsTotal']
        country = datatype.COUNTRY(date=date,name=name,continent=continent,confirmed=confirmed,cures=cures,deaths=deaths)
        session.add(country)
       
    # 世界总数据
    total = overseas['total']
    # print(total)
    date = datetime.date.today()
    confirmed = total['confirmedTotal']
    cures = total['curesTotal']
    deaths= total['deathsTotal']
    world = datatype.WORLDTOTAL(date=date,confirmed=confirmed,cures=cures,deaths=deaths)
    session.add(world)

    session.commit() # 修改数据库

getdata_api()

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
    data['province'] = data['province'].apply(lambda x:f[x])
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
    return data_ch

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
    # update_all()
    getdata_api()
    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()  
    # 添加调度任务
    scheduler.add_job(getdata_api , 'interval', seconds=time)
    # 启动调度任务
    scheduler.start()



