"""
Routes and views for the flask application.
"""
import time
import json
from datetime import datetime , date , timedelta
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from nCovNews import app , db
from nCovNews import datatype , data_predict , user_mod , forms

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

from nCovNews.data_update import flags 

@app.route('/overview')
def overview():
    """Renders the home page."""
    today = date.today()
    oversea = datatype.COUNTRY.query.filter_by(date = today).all()
    return render_template(
        'overview.html',
        title='Overview',
        year=datetime.now().year,
        message='Your overview page.',
        oversea=oversea,
        flags=flags,
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
    chinaInc = {'confirmedtotal':[],'confirmedexist':[],'suspected':[],'cures':[],'deaths':[],'asymptomatic':[]}
    chinaPredict = {'confirmedtotal':[],'confirmedexist':[],'suspected':[],'cures':[],'deaths':[],'asymptomatic':[]}
    for item in chinatotal:
        timeseries.append(str(item.date))
        china['confirmedtotal'].append([str(item.date),item.confirmed])
        china['confirmedexist'].append([str(item.date),item.confirmed-item.cures-item.deaths])
        china['cures'].append([str(item.date),item.cures])
        china['suspected'].append([str(item.date),item.suspected])
        chinaInc['suspected'].append([str(item.date),item.suspectedInc])# 新增疑似
        china['deaths'].append([str(item.date),item.deaths])
        china['asymptomatic'].append([str(item.date),item.asymptomatic])  
    # 计算变化量(不含疑似)
    for i in range(len(chinatotal)-1):
        chinaInc['confirmedtotal'].append([timeseries[i+1],china['confirmedtotal'][i+1][1]-china['confirmedtotal'][i][1]])
        chinaInc['confirmedexist'].append([timeseries[i+1],china['confirmedexist'][i+1][1]-china['confirmedexist'][i][1]])
        chinaInc['cures'].append([timeseries[i+1],china['cures'][i+1][1]-china['cures'][i][1]])
        chinaInc['deaths'].append([timeseries[i+1],china['deaths'][i+1][1]-china['deaths'][i][1]])
        chinaInc['asymptomatic'].append([timeseries[i+1],china['asymptomatic'][i+1][1]-china['asymptomatic'][i][1]])
    # 构造预测序列
    predictseries = []
    dt = 100 # 预测天数
    for i in range(0,len(chinatotal)+dt):
        if i<len(chinatotal):
            predictseries.append(chinatotal[i].date)
        else:
            predictseries.append(predictseries[i-1]+timedelta(days = 1))
    for i in range(0,len(chinatotal)+dt):
        predictseries[i] = str(predictseries[i])
    # 趋势预测
    chinaPredict['confirmedtotal']=data_predict.result2(predictseries,china['confirmedtotal'],0.55)
    chinaPredict['confirmedexist']=data_predict.result2(predictseries,china['confirmedexist'],0.4)
    # 地图数据
    province = datatype.PROVINCE.query.filter_by(date=date.today())
    map = {'confirmedtotal':[],'confirmedexist':[],'cures':[],'deaths':[],'asymptomatic':[]}
    for item in province:
        map['confirmedtotal'].append({'name':item.name,'value':item.confirmed})
        map['confirmedexist'].append({'name':item.name,'value':item.confirmed-item.cures-item.deaths})
        map['cures'].append({'name':item.name,'value':item.cures})
        map['deaths'].append({'name':item.name,'value':item.deaths})
        map['asymptomatic'].append({'name':item.name,'value':item.asymptomatic})
    return json.dumps({'timeseries':timeseries,
                       'predictseries':predictseries,
                       'china':china,
                       'chinaInc':chinaInc,
                       'chinaPredict':chinaPredict
                       ,'map':map
                       },ensure_ascii=False)

@app.route('/delete_all_discuss')
def delete_all_discuss():
    user_mod.delete_all()
    return redirect(url_for('about'))

# 登陆表单
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        id = form.id.data
        return redirect(url_for('home'))
    return render_template('login.html',
                           title='Login', 
                           form=form, )

# 注册表单
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        session = db.session
        id = form.id.data
        name = form.name.data
        password = form.password.data
        user = datatype.USER(id=id,name=name,password=password)
        session.add(user)
        session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Register', 
                           form=form, )

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


