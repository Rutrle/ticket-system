from smart_ticket import app
from flask import render_template, Response


@app.route('/')
def home_page() -> Response:
    """
    simple home page
    """
    return render_template('index.html')


@app.route('/about')
def about_page() -> Response:
    """
    page with information about SmartTicket
    """
    return render_template('about.html')
