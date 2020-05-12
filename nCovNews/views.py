"""
Routes and views for the flask application.
"""

from datetime import datetime
from datetime import date
from datetime import timedelta
from flask import render_template
from nCovNews import app
from nCovNews import db
from nCovNews import datatype

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    today = date.today()
    yesterday = today + timedelta(days = -1)
    # 中国数据查询
    cn = datatype.CHINATOTAL.query.filter_by(date = today).first()
    if (cn is None):
           cn = datatype.CHINATOTAL.query.filter_by(date = yesterday).first()
    # 世界数据查询
    wd = datatype.WORLDTOTAL.query.filter_by(date = today).first()
    if (cn is None):
           wd = datatype.WORLDTOTAL.query.filter_by(date = yesterday).first()

    return render_template(
        'index.html',
        title='主页',
        year=datetime.now().year,
        cn_date=cn.date,cn_confirmed=cn.confirmed,cn_suspected=cn.suspected,cn_cures=cn.cures,cn_deaths=cn.deaths,cn_asymptomatic = cn.asymptomatic,
        wd_date=wd.date,wd_confirmed=wd.confirmed,wd_cures=wd.cures,wd_deaths=wd.deaths,
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
    return render_template(
        'discuss.html',
        title='Discuss',
        year=datetime.now().year,
        message='Your application description page.'
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
    """Renders the about page."""
    return render_template(
        'overview.html',
        title='Ooverviewverview',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/share')
def share():
    """Renders the about page."""
    return render_template(
        'share.html',
        title='Share',
        year=datetime.now().year,
        message='Your share page.'
    )

@app.route('/news')
def news():
    """Renders the about page."""
    return render_template(
        'news.html',
        title='News',
        year=datetime.now().year,
        message='Your news page.'
    )


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