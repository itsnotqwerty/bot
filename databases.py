import sqlite3


class DatabaseInterface:

    def __init__(self):
        self.dbs = {}
        self.active_db = None

    def connect(self, db_name):
        db = sqlite3.connect(f'files/databases/{db_name}.db')
        self.dbs[db_name] = db
        self.active_db = db

    def create_table(self, table, values):
        db = self.active_db
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} {values}")
        cursor.close()

    def extend_table(self, table, column):
        db = self.active_db
        cursor = db.cursor()
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column};")
        cursor.close()

    def lookup_one(self, table, key, value):
        db = self.active_db
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {key}={value};")
        entry = cursor.fetchone()
        cursor.close()
        return entry

    def lookup_many(self, table, key, value):
        db = self.active_db
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {key}={value};")
        entries = cursor.fetchall()
        cursor.close()
        return entries

    def insert_one(self, table, values):
        db = self.active_db
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO {table} VALUES {values};")
        db.commit()
        cursor.close()

    def delete_many(self, table, key, value):
        db = self.active_db
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE {key}={value};")
        db.commit()
        cursor.close()
