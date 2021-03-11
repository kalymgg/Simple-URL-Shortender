import flask
import sqlite3 as sql
import datetime

connection = sql.connect("data.db", check_same_thread=False)
cursor = connection.cursor()

app = flask.Flask(__name__)

try:
  cursor.execute("""CREATE TABLE urls(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    redirect text)""")
except:
  pass

@app.route("/u/<uid>", methods=["GET"])
def get_my_ip(uid):
	id = uid
	time = datetime.datetime.now()
	ip = flask.request.remote_addr
	cursor.execute(f"INSERT INTO url_{id}(time, ip) VALUES('{time}', '{ip}')")
	cursor.execute(f"SELECT redirect FROM urls WHERE id = {id}")
	connection.commit()
	return f'<script>window.location.href = "{cursor.fetchall()[0][0]}";</script>'

@app.route('/cut/', methods=["GET"])
def cut():
	url = flask.request.args['url']
	cursor.execute(f"SELECT id FROM urls WHERE redirect = '{url}'")
	data = cursor.fetchall()
	if cursor.fetchall() == []:
		cursor.execute(f"INSERT INTO urls(redirect) VALUES('{url}')")
		print(f"INSERT INTO urls(redirect) VALUES('{url}')")
		connection.commit()
	cursor.execute(f"SELECT id FROM urls WHERE redirect = '{url}'")
	data = cursor.fetchall()
	print(data[0][0])
	try:
		print(f"CREATE TABLE url_{data[0][0]}(click_id INTEGER PRIMARY KEY AUTOINCREMENT, time text, ip text)")
		cursor.execute(f"CREATE TABLE url_{data[0][0]}(click_id INTEGER PRIMARY KEY AUTOINCREMENT, time text, ip text)")
		connection.commit()
	except Exception as e:
		print(e)
	return f'{data[0][0]}'

app.run(host='0.0.0.0',port=8080)