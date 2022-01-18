import sqlite3


def db_connect(name='bot'):
    db = sqlite3.connect(f'files/databases/{name}.db')
    return db


def db_lookup(db, key, value):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE :key=:value;", {'key': key, 'value': value})
    user = cursor.fetchone()
    cursor.close()
    return user




