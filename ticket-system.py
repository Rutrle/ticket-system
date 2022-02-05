from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    #testing view, to be deleted
    return render_template('base.html')

@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


app.run(debug=True)
