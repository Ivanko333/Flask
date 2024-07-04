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


@app.route('/add_article')
def add_article():
    return render_template('add_article.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
