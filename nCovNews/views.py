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
from nCovNews import app
from nCovNews import db
from nCovNews import datatype
from nCovNews import user_mod

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""  
    return render_template(
        'index.html',
        title='主页',
        year=datetime.now().year, 
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

@app.route('/discuss',methods=['GET','POST'])
def discuss():
    """Renders the about page."""
    if request.method == 'POST':
        word = request.form.get('word')
        user_mod.post_word(word)
    dislist = datatype.DISCUSS.query.all()
    return render_template(
        'discuss.html',
        title='Discuss',
        year=datetime.now().year,
        message='Your application description page.',
        dislist = dislist,
    )

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
        'overview.html',
        title='Overview',
        year=datetime.now().year,
        chinatotal=chinatotal,
        worldtotal=worldtotal,
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
    # 中国数据查询
    chinatotal = datatype.CHINATOTAL.query.all()
    datalist = []
    xseries = []
    for item in chinatotal:
        data=[str(item.date),item.confirmed]
        datalist.append(data)
        xseries.append(str(item.date))
    return json.dumps({'data':datalist,'xseries':xseries})



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




