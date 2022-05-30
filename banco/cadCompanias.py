import sqlite3 

banco = sqlite3.connect('cadCompanias.db')
cursor = banco.cursor()

sql = '''CREATE TABLE IF NOT EXISTS cadCompanias(
		id_compania INTEGER PRIMARY KEY AUTOINCREMENT,
		valorfixo text,
		dataEntrega text,
  		valorUnidade text,
  		DistKM text,
  		total text);'''

cursor.execute(sql)
banco.commit()		