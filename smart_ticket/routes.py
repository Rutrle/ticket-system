from smart_ticket import app
from flask import render_template


@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')