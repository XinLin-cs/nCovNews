import time
import datetime
import json
import requests
import pandas as pd
import numpy as np
import _thread

from nCovNews import db
from nCovNews import datatype

def getdata_api():
    session = db.session

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
        # 与数据库合并
        province = datatype.PROVINCE.query.filter_by(date=date,name=name).first()
        if province is None:
            province = datatype.PROVINCE(date=date,name=name,confirmed=confirmed,cures=cures,deaths=deaths,asymptomatic=asymptomatic)
            session.add(province)
        else:
            province.confirmed = confirmed
            province.cures = cures
            province.deaths = deaths
            province.asymptomatic = asymptomatic

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
        # 与数据库合并
        chinatotal = datatype.CHINATOTAL.query.filter_by(date=date).first()
        if chinatotal is None:
            chinatotal = datatype.CHINATOTAL(date=date,confirmed=confirmed,suspected=suspected,cures=cures,deaths=deaths,asymptomatic=asymptomatic)
            session.add(chinatotal)
        else:
            chinatotal.confirmed = confirmed
            chinatotal.cures = cures
            chinatotal.deaths = deaths
            chinatotal.asymptomatic = asymptomatic

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
        # 与数据库合并
        country = datatype.COUNTRY.query.filter_by(date=date,name=name).first()
        if country is None:
            country = datatype.COUNTRY(date=date,name=name,continent=continent,confirmed=confirmed,cures=cures,deaths=deaths)
            session.add(country)
        else:
            country.confirmed = confirmed
            country.cures = cures
            country.deaths = deaths
       
    # 世界总数据
    total = overseas['total']
    # print(total)
    date = datetime.date.today()
    confirmed = total['confirmedTotal']
    cures = total['curesTotal']
    deaths= total['deathsTotal']
    # 与数据库合并
    world = datatype.WORLDTOTAL.query.filter_by(date=date).first()
    if world is None:
        world = datatype.WORLDTOTAL(date=date,confirmed=confirmed,cures=cures,deaths=deaths)
        session.add(world)
    else:
        world.confirmed = confirmed
        world.cures = cures
        world.deaths = deaths

    session.commit() # 修改数据库

def get_news( page , num ):
    session = db.session
    url = 'http://lab.isaaclin.cn/nCoV/api/news?page=%d&num=%d' % ( page , num )
    try:
        respone = requests.get(url).json()
        time.sleep(1)
        msg = respone['results']
        for data in msg:
            date = float(data['pubDate'])/1000
            title = data['title']
            summary = data['summary']
            info = data['infoSource']
            url = data['sourceUrl']
            news = datatype.NEWS(date=date,title=title,summary=summary,info=info,url=url)
            session.add(news)
        session.commit()
    except:
        return 0

get_news

def get_fakenews( page , num ):
    session = db.session
    url = 'http://lab.isaaclin.cn/nCoV/api/rumors?page=%d&num=%d&rumorType=%d' % ( page , num , 0 )
    try:
        respone = requests.get(url).json()
        time.sleep(1)
        msg = respone['results']
        for data in msg:
            title = data['title']
            summary = data['mainSummary']
            info = data['body']
            news = datatype.FAKENEWS(title=title,summary=summary,info=info)
            session.add(news)
        session.commit()
    except:
        return 0

def get_information( page , num ):
    session = db.session
    url = 'http://lab.isaaclin.cn/nCoV/api/rumors?page=%d&num=%d&rumorType=%d' % ( page , num , 1 )
    try:
        respone = requests.get(url).json()
        time.sleep(1)
        msg = respone['results']
        for data in msg:
            title = data['title']
            summary = data['mainSummary']
            info = data['body']
            news = datatype.INFORMATION(title=title,summary=summary,info=info)
            session.add(news)
        session.commit()
    except:
        return 0

# 历史数据
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

from apscheduler.schedulers.background import BackgroundScheduler

def update_all():
    try:
        starttime = datetime.datetime.today()
        print('[Updatedata] updating start!')
        # 测试代码=====
        # db.drop_all()
        # db.create_all() 
        #==============
        print('[Updatedata] start at %s' % ( starttime.isoformat(sep=' ') ) )
        getdata_api()
        print('[Updatedata] updating for 70%')
        get_news(1,10)
        print('[Updatedata] updating for 80%')
        get_information(1,10)
        print('[Updatedata] updating for 90%')
        get_fakenews(1,10)
        print('[Updatedata] updating for 100%')
    except BaseException as err:
        print(err)
    except:
        pass
    else:
        pass
    finishtime = datetime.datetime.today()
    print('[Updatedata] last for %d seconds' %  ( finishtime - starttime ).seconds )
    print('[Updatedata] updating finished! ')

def auto_update(time):
    _thread.start_new_thread(update_all)
    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()  
    # 添加调度任务
    scheduler.add_job(update_all , 'interval', seconds=time)
    # 启动调度任务
    scheduler.start()



