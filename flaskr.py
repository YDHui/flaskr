import os
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
from db_connect import MysqlOprate
import sha
secret_key = os.urandom(24)
app = Flask(__name__)
app.config.from_object(__name__)



app.config.update(dict(
	DATABASE=os.path.join(app.root_path,'flaskr.db'),
	SECRET_KEY=secret_key,
	USERNAME='admin',
	PASSWORD='fql123'
	))
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

@app.before_request
def before_reques():
	g.db = MysqlOprate("localhost","flask_test","123test",3306)

# @app.teardown_request
# def teardown_request(exception):
# 	db = getattr(g,'db',None)
# 	if db is not None:
# 		db.conn_close()

@app.route("/")
def show_entries():
	#db = MysqlOprate("localhost","flask_test","123test",3306)
	data = g.db.data_query('''select Ftitle,Ftext from test.t_entries order by Fid desc''' )
	#cur = g.db.execute('select title,text from entries order by id desc')
	entries = list(data)
	return render_template("show_entries.html",entries=entries)

@app.route("/add",methods=["POST"])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	#db.execute("insert into entries (title,text) values (?,?)",[request.form["title"],request.form["text"]])
	sql = ''' insert into test.t_entries (Ftitle,Ftext) values ("%s","%s")'''%(request.form["title"],request.form["text"])
	ret = g.db.dml_exec(sql)
	if ret == 0:
		flash('New entry was successfully posted')
	else:
		flash('Failed to post')
	return redirect(url_for('show_entries'))

@app.route("/login",methods=["GET","POST"])
def login():
	s_login = sha.new()
	error = None
	login_sql = ''
	if request.method == "POST":
		login_sql = '''select * from test.t_user_info where Fusername="%s"'''%(request.form['username'])
		user_info = g.db.data_query(login_sql)
		s_login.update(request.form['password'])
		if len(user_info) == 0:
		#if request.form['username'] != app.config['USERNAME']:
			error = 'invalid username'
		#elif request.form['password'] != app.config['PASSWORD']:
		elif s_login.hexdigest() != user_info[0]["Fpassword"]:
			error = 'invalid password'
		else:
			session['logged_in'] = True
			flash('You are logged_in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)

@app.route("/register",methods=["GET","POST"])
def register():
	error = None
	check_sql = ''
	add_sql = ''
	s = sha.new()
	if request.method == "POST":
		check_sql = '''select * from test.t_user_info where Fusername="%s" '''%(request.form["username"])
		check_res = g.db.data_query(check_sql)
		if len(check_res) != 0:
			error = 'username is exist'
		else:
			s.update(request.form["password"])
			handle_pass = s.hexdigest()
			add_sql = '''insert into test.t_user_info (Fusername,Fpassword) values ("%s","%s")'''%(request.form["username"],handle_pass)
			ret = g.db.dml_exec(add_sql)
			if ret == 0:
				return redirect(url_for('show_entries'))
	return render_template('register.html',error=error)

@app.route("/logout")
def logout():
	session.pop("logged_in",None)
	flash("You have logged out")
	return redirect(url_for("show_entries"))
if __name__ == "__main__":
	app.run()