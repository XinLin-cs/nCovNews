"""
Routes and views for the flask application.
"""
import time
import json
from datetime import datetime
from datetime import date
from datetime import timedelta
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from nCovNews import app
from nCovNews import db
from nCovNews import datatype
from nCovNews import user_mod

@app.route('/')

@app.route('/home')
def home():
    """Renders the home page."""
    today = date.today()
    # 中国数据查询
    chinatotal = datatype.CHINATOTAL.query.filter_by(date = today).first()
    if (chinatotal is None):
        today = today + timedelta(days = -1)
        chinatotal = datatype.CHINATOTAL.query.filter_by(date = today).first()
        if (chinatotal is None):
            today = today + timedelta(days = -1)
            chinatotal = datatype.CHINATOTAL.query.filter_by(date = today).first()
    # 世界数据查询
    today = date.today()
    worldtotal = datatype.WORLDTOTAL.query.filter_by(date = today).first()
    if (worldtotal is None):
        today = today + timedelta(days = -1)   
        worldtotal = datatype.WORLDTOTAL.query.filter_by(date = today).first()
    
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
        chinatotal=chinatotal,
        worldtotal=worldtotal,
        message='Your home page.'
       
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/discuss')
def discuss():
    """Renders the about page."""
    dislist = datatype.DISCUSS.query.all()
    dislist.sort(key=lambda x:x.date,reverse=True)
    return render_template(
        'discuss.html',
        title='Discuss',
        year=datetime.now().year,
        message='Your application description page.',
        dislist = dislist,
    )

@app.route('/postword',methods=['POST'])
def postword():
    """Renders the about page."""
    name = request.form.get('name')
    word = request.form.get('word')
    user_mod.post_word(name,word)
    return  redirect(url_for('discuss'))

@app.route('/analyze')
def analyze():
    """Renders the about page."""
    return render_template(
        'analyze.html',
        title='Analyze',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/overview')
def overview():
    """Renders the home page."""
    
    return render_template(
        'overview.html',
        title='Overview',
        year=datetime.now().year,
        message='Your overview page.'
       
    )



@app.route('/news')
def news():
    """Renders the about page."""
    # 新闻数据查询
    news = datatype.NEWS.query.all()
    fakenews = datatype.FAKENEWS.query.all()
    information = datatype.INFORMATION.query.all()
    return render_template(
        'news.html',
        time = time,
        title='News',
        year=datetime.now().year,
        message='Your news page.',
        news=news,
        fakenews=fakenews,
        information=information,
        
    )

# 数据接口
@app.route('/getdata')
def getdata():
    # 中国数据
    chinatotal = datatype.CHINATOTAL.query.all()
    chinatotal.sort(key=lambda x:x.date)
    timeseries = []
    china = {'confirmedtotal':[],'confirmedexist':[],'suspected':[],'cures':[],'deaths':[],'asymptomatic':[]}
    for item in chinatotal:
        timeseries.append(str(item.date))
        china['confirmedtotal'].append([str(item.date),item.confirmed])
        china['confirmedexist'].append([str(item.date),item.confirmed-item.cures])
        china['cures'].append([str(item.date),item.cures])
        china['suspected'].append([str(item.date),item.suspected])
        china['deaths'].append([str(item.date),item.deaths])
        china['asymptomatic'].append([str(item.date),item.asymptomatic])
    # 地图数据
    province = datatype.PROVINCE.query.filter_by(date=date.today())
    map = {'confirmedtotal':{},'confirmedexist':{},'cures':{},'deaths':{},'asymptomatic':{}}
    for item in province:
        map['confirmedtotal'][item.name]=item.confirmed
        map['confirmedexist'][item.name]=item.confirmed-item.cures
        map['deaths'][item.name]=item.deaths
        map['asymptomatic'][item.name]=item.asymptomatic
    return json.dumps({'timeseries':timeseries,'china':china,'map':map},ensure_ascii=False)



#没用的




@app.route('/test')
def test():
    """Renders the about page."""
    return render_template(
        'test.html',
        title='Test',
        year=datetime.now().year,
        message='Your test page.'
    )

@app.route('/temp')
def temp():
    """Renders the about page."""
    return render_template(
        'temp.html',
        title='Temp',
        year=datetime.now().year,
        message='Your temp page.'
    )


