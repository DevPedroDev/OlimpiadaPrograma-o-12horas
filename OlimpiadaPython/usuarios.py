import sqlite3

banco = sqlite3.connect('user.db')
cursor = banco.cursor()

sql = '''CREATE TABLE IF NOT EXISTS user(
id_user INTEGER PRIMARY KEY AUTOINCREMENT,
usuario text,
senha text);'''

cursor.execute(sql)
banco.commit()