from flask import Flask, render_template
import db

app = Flask(__name__)


@app.route('/')
def index():
    info = db.get_info()
    return render_template('main.html', info=info)


@app.route('/about')
def about():
    return render_template('about.html')
