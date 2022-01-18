import sqlite3

db = sqlite3.connect('bot.db')
cursor = db.cursor()
cursor.execute("""
    INSERT INTO users VALUES (
    'Apollyon',
    0727,
    109094301962625024,
    1,
    0
    )
""")

for user in cursor.execute("SELECT * FROM users"):
    print(user)
db.commit()
db.close()


