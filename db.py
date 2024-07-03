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
                   'content TEXT)')
    db.commit()


def add_info(title, topic, content):
    today = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
    cursor.execute('INSERT INTO article(title, date, topic, content) VALUES(?, ?, ?, ?)', (title, today, topic, content))
    db.commit()


def edit_info(id, title, topic, content):
    today = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
    cursor.execute('UPDATE article SET title=?, date=?, topic=?, content=? WHERE id=?', (title, today, topic, content, id))
    db.commit()


def delete_info(id):
    cursor.execute('DELETE FROM article WHERE id=?', (id,))
    db.commit()


def get_info():
    cursor.execute('SELECT * FROM article')
    return cursor.fetchall()


create_table()

