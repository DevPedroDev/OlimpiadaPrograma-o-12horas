
from flask import Flask, render_template, request, session, redirect, url_for
import os, sqlite3
import smtplib, hashlib
from email.message import EmailMessage
from senha import senha

app = Flask(__name__,template_folder='view', static_folder='view', static_url_path='')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/", methods=['GET', 'POST'])
def Index():
	return render_template('index.html')


@app.route("/email", methods=['GET', 'POST'])
def enviar_email():
	resultado = 0
	try:
		if request.method == 'POST':
			my_email = 'olimpiadaudf@gmail.com'
			senhaEmail = senha
			msg = EmailMessage()
			#msg['Subject'] = request.form['email']
			msg['Subject'] = request.json['email']
			msg['From'] = 'olimpiadaudf@gmail.com'
			msg['To'] = 'olimpiadaudf@gmail.com'
			#msg.set_content(request.form['message'])
			msg.set_content(request.json['mensagem'])

			with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
				smtp.login(my_email, senhaEmail)
				smtp.send_message(msg)
			resultado = 1
			print("O resultado foi " + str(resultado))
	except:
		pass		
	
	return str(resultado)


def buscar_companhias():
	banco = sqlite3.connect('cadCompanias.db')
	cursor = banco.cursor()
	sql = "SELECT id_compania, valorfixo, dataEntrega, valorUnidade, DistKM,  total FROM cadCompanias"
	resultado = False
	try:
		resultado = cursor.execute(sql).fetchall()
		banco.commit()
		banco.close()
	except Exception as e:
		print(e)
	return resultado

def buscar_companhia(id):
	banco = sqlite3.connect('cadCompanias.db')
	cursor = banco.cursor()
	sql = "SELECT id_compania, valorfixo, dataEntrega, valorUnidade, DistKM, total FROM cadCompanias WHERE id_compania = " + str(id)
	resultado = False
	try:
		resultado = cursor.execute(sql).fetchone()
		banco.commit()
		banco.close()
	except Exception as e:
		print(e)
	return resultado

@app.route("/logado")
def logado():
	if 'username' not in session:
		return render_template("login.html")
	usuario=session['username']
	banco = sqlite3.connect('cadUser.db')
	cursor = banco.cursor()
	sql = "SELECT * FROM cadUser WHERE email = '{}' and admin = 'admin'".format(usuario)
	cursor.execute(sql)
	print(sql)
	resultados = cursor.fetchone()
	try:
		if 'Logado' in session:
			print(session['Logado'])
			print(resultados)
			if session['Logado'] == True and resultados:
				print("1")
				return render_template('admin.html', companias=buscar_companhias())
			elif session['Logado'] == True:
				print("2")
				return render_template("logado.html", usuario=usuario, compania='0')	
			else:
				print("3")
				return render_template("login.html")
		else:
			print("4")
			return render_template("login.html")

	except Exception as e:
		print(e)
	return render_template("login.html")


@app.route("/login", methods=['POST'])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		hash = hashlib.md5(password.encode())
		senha = hash.hexdigest()

		banco = sqlite3.connect('cadUser.db')
		cursor = banco.cursor()
		sql = "SELECT * FROM cadUser WHERE email = '{}' and senha = '{}'".format(username, senha)
		cursor.execute(sql)
		banco.commit()
		resultado = cursor.fetchall()
		for login in resultado:
			if username == login[1] and senha == login[4]:
				session['Logado'] = True
				session['username'] = username
				return redirect(url_for("logado"))
			else:
				msg = "Usuário ou senha incorretos"
	return render_template("login.html")

@app.route("/logout")
def logout():
	session.clear()
	return render_template('login.html')

@app.route("/cadastro", methods= ["POST"])
def cadastro():
	if request.method == "POST":
		email = request.form['email']
		cpf = request.form['cpf']
		dtNasc = request.form['dtNasc']
		senha = request.form['pass']
		hash = hashlib.md5(senha.encode())
		senha = hash.hexdigest()
  
		banco = sqlite3.connect('cadUser.db')
		cursor = banco.cursor()
		sql = "INSERT INTO cadUser(email, cpf, dtNasc, senha) VALUES('{}', '{}', '{}', '{}')".format(email, cpf, dtNasc, senha)

		try:
			cursor.execute(sql)
			banco.commit()
			banco.close()
		except Exception as e:
			print(e)	
			

	return render_template('logado.html')	

@app.route("/cadastrarCompanias", methods=["POST"])
def cadastrarCompanias():
	if request.method == "POST":
		dataEntrega = request.form['dataEntrega']
		valorUnidade = request.form['valorUnidade']
		DistKM = request.form['DistKM']
		valorfixo = 1000
		total = 0


		dataEntrega = int(dataEntrega)
		valorUnidade = int(valorUnidade)
		DistKM = int(DistKM)
		valorfixo = int(valorfixo)
		total = 0

		if dataEntrega == 1:
			total = valorfixo+(valorfixo*valorUnidade)+(1*DistKM)
			total2 = (total*0.3)+total
		elif dataEntrega == 2:
			total = valorfixo+(valorfixo*valorUnidade)+(1*DistKM)
			total2 = (total*0.3)+total
		elif dataEntrega == 3:
			total = valorfixo+(valorfixo*valorUnidade)+(1*DistKM)
			total2 = (total*0.3)+total

		elif dataEntrega == 4:
			total = valorfixo+(valorfixo*valorUnidade)+(1*DistKM)
			total2 = (total*0.3)+total
				

		banco = sqlite3.connect('cadCompanias.db')
		cursor = banco.cursor()
		sql = "INSERT INTO cadCompanias(valorfixo, dataEntrega, valorUnidade, DistKM,  total) VALUES('{}', '{}', '{}', '{}', '{}')".format( valorfixo, dataEntrega, valorUnidade, DistKM, total2)

		try:
			cursor.execute(sql)
			banco.commit()
			banco.close()
		except Exception as e:
			print(e)	
	return render_template('ocean.html')


@app.route('/alterar', methods=["POST"])
def alterar():
	if request.method == "POST":
		dataEntrega = request.form['dataEntrega']
		valorUnidade = request.form['valorUnidade']
		DistKM = request.form['DistKM']
		id_compania = request.form['id_compania']
  
		banco = sqlite3.connect('cadCompanias.db')
		cursor = banco.cursor()
		sql = "UPDATE cadCompanias SET valorfixo = '1000', dataEntrega = '{}', valorUnidade = '{}', DistKM = '{}' WHERE id_compania = {}".format(dataEntrega, valorUnidade, DistKM, id_compania)

		try:
			cursor.execute(sql)
			banco.commit()
			banco.close()
		except Exception as e:
			print(e)	
			
	return redirect(url_for('logado'))


@app.route('/editar/<id>')
def editar(id):
	return render_template('logado.html', compania=buscar_companhia(id))


@app.route('/deletar/<id>')
def deletar(id):
	banco = sqlite3.connect('cadCompanias.db')
	cursor = banco.cursor()
	sql = "DELETE FROM cadCompanias WHERE id_compania = {}".format(id)

	try:
		cursor.execute(sql)
		banco.commit()
		banco.close()
	except Exception as e:
		print(e)
	
	return redirect(url_for('logado'))


if __name__ == '__main__':
	app.run(port=8080, debug=True)	