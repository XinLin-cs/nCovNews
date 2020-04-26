"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from nCovNews import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='主页',
        year=datetime.now().year,
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

