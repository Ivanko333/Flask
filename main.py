from flask import Flask, render_template, request, redirect
import db
from forms import ArticleForm


app = Flask(__name__)


@app.route('/')
def index():
    info = db.get_info()
    return render_template('main.html', info=info)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_article', methods=("GET", "POST"))
def add_article():
    form = ArticleForm(request.form)
    if request.method == "GET":
        return render_template('add_article.html', form=form)
    if request.method == "POST":
        if form.validate():
            db.add_info(form.title.data, form.topic.data, form.text.data)
            return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
