import sqlite3
import datetime

db = sqlite3.connect("schema.db", check_same_thread=False)
cursor = db.cursor()


def create_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS article('
                   'id INTEGER PRIMARY KEY UNIQUE NOT NULL,'
                   'title STR,'
                   'date STR,'
                   'topic STR,'
                   'content TEXT,'
                   'user_id INTEGER,'
                   'FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE)')
    cursor.execute("CREATE TABLE IF NOT EXISTS users("
                   "id INTEGER PRIMARY KEY UNIQUE NOT NULL,"
                   "name STR NOT NULL,"
                   "username STR UNIQUE NOT NULL,"
                   "password STR NOT NULL)")

    db.commit()


def add_info(title, topic, content, user_id):
    today = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
    cursor.execute('INSERT INTO article(title, date, topic, content, user_id) VALUES(?, ?, ?, ?, ?)',
                   (title, today, topic, content, user_id))
    db.commit()


def edit_info(id, title, topic, content):
    today = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
    cursor.execute('UPDATE article SET title=?, date=?, topic=?, content=? WHERE id=?',
                   (title, today, topic, content, id))
    db.commit()


def delete_info(id):
    cursor.execute('DELETE FROM article WHERE id=?', (id,))
    db.commit()


def get_info():
    cursor.execute('SELECT * FROM article')
    return cursor.fetchall()


def get_article(id):
    cursor.execute('SELECT * FROM article WHERE id=?', (id, ))
    return cursor.fetchone()


def add_user(name, username, password):
    cursor.execute('INSERT INTO users(name, username, password) VALUES(?, ?, ?)', (name, username, password))
    db.commit()
    return cursor.lastrowid


def check_user(username, password):
    cursor.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
    user_id = cursor.fetchone()
    if user_id:
        return user_id[0]
    else:
        return None


create_table()

