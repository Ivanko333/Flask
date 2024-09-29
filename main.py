from flask import Flask, render_template, request, redirect
import db
from forms import ArticleForm, UserForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, user_loaded_from_request, current_user

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
    # print(info[1][5] == current_user.get_id())
    # print(type(info[1][5]))
    # print(type(current_user.get_id()))
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
            db.add_info(form.title.data, form.topic.data, form.text.data, current_user.get_id())
            return redirect('/')


@app.route('/register', methods=("GET", "POST"))
def register():
    form = UserForm(request.form)
    if request.method == "GET":
        return render_template('register.html', form=form)

    if request.method == "POST":
        if form.validate():
            user_id = db.add_user(form.name.data, form.username.data, form.password.data)
            login_user(User(user_id))
        return redirect('/')


@app.route('/<int:id>', methods=("GET", "POST"))
@login_required
def edit_article(id):
    if int(current_user.get_id()) == db.get_article(id)[5]:
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
    else:
        return '403'


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/login', methods=("GET", "POST"))
def login():
    form = UserForm(request.form)
    if request.method == "POST":
        id = db.check_user(form.username.data, form.password.data)
        if id:
            login_user(User(id))
            return redirect('/')
        else:
            pass

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
