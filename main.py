from flask import Flask, render_template, request, redirect
import db
from forms import ArticleForm, UserForm
from flask_login import LoginManager, UserMixin, login_required, login_user

app = Flask(__name__)
app.secret_key = 'secret_key'
login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def index():
    info = db.get_info()
    return render_template('main.html', info=info)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_article', methods=("GET", "POST"))
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == "GET":
        return render_template('add_article.html', form=form)
    if request.method == "POST":
        if form.validate():
            db.add_info(form.title.data, form.topic.data, form.text.data)
            return redirect('/')


@app.route('/register', methods=("GET", "POST"))
def register():
    form = UserForm(request.form)
    if request.method == "GET":
        return render_template('register.html', form=form)

    if request.method == "POST":
        if form.validate():
            db.add_user(form.name.data, form.username.data, form.password.data)
        return redirect('/')


@app.route('/<int:id>', methods=("GET", "POST"))
def edit_article(id):
    form = ArticleForm(request.form)
    if request.method == "GET":
        try:
            info = db.get_article(id)
            form.title.data = info[1]
            form.topic.data = info[3]
            form.text.data = info[4]
        except TypeError:
            return redirect('/')
        return render_template('edit_article.html', form=form)
    if request.method == "POST" and "edit" in request.form:
        if form.validate():
            db.edit_info(id, form.title.data, form.topic.data, form.text.data)
            return redirect('/')
    if request.method == "POST" and "delete" in request.form:
        db.delete_info(id)
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
