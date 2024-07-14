from wtforms.fields import StringField, TextAreaField, SelectField, PasswordField
from wtforms.form import Form
from wtforms import validators


class ArticleForm(Form):
    title = StringField("title", (validators.length(max=50), validators.data_required()))
    text = TextAreaField("text", (validators.data_required(),))
    topic = SelectField('topic', choices=[('Новости', "Новости"),
                                          ('Игры', "Игры"),
                                          ('Развлечения', "Развлечения"),
                                          ('Программирование', 'Программирование'),
                                          ('Образование', 'Образование'),
                                          ('Музыка', 'Музыка')])


class UserForm(Form):
    name = StringField("name", (validators.data_required(),))
    username = StringField("username", (validators.data_required(),))
    password = PasswordField("password", (validators.data_required(),))
