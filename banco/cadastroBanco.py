import sqlite3 


banco = sqlite3.connect('cadUser.db')
cursor = banco.cursor()

sql = '''CREATE TABLE IF NOT EXISTS cadUser(
		id_cad INTEGER PRIMARY KEY AUTOINCREMENT,
		email text,
		cpf text,
		dtNasc text,
		senha text,
  		admin text);'''

cursor.execute(sql)
banco.commit()		