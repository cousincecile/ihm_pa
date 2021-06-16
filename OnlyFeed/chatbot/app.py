from flask import Flask, jsonify, make_response, render_template, request, redirect
from flask_bootstrap import Bootstrap
from models import db, Base, Chatbot_User, Chatbot_message_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS, cross_origin
import datetime
import json
import psycopg2
from functions import days_between, get_games_to_compare


app = Flask(__name__)
CORS(app)
Bootstrap(app)

POSTGRES = {
    'user': 'of_dck',
    'pw': 'gft78kP9!luY!',
    'db': 'onlyfeed',
    'host': 'onlyfeed.ddns.net',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db = SQLAlchemy(app)
conn = psycopg2.connect( host=POSTGRES['host'], user=POSTGRES['user'], password=POSTGRES['pw'], dbname=POSTGRES['db'])
data = []

@app.route("/add_user",  methods=['POST'])
def add_user():
  email = request.form.get('email')
  username = request.form.get('username')
  age = request.form.get('age')

  new_user = Chatbot_User(username = username, email = email, age= age)

  try:
    db.session.add(new_user)
    db.session.commit()
    added_user = db.session.query(Chatbot_User).filter_by(email=email).first()
    data = {'message': added_user.toJSON(), 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)

  except Exception as e:
    data = {'message': e, 'code': 'ERROR'}
    return make_response(jsonify(data))


@app.route("/add_user_message",  methods=['POST'])
def add_user_message():
  id_user = request.form.get('userID')
  content = request.form.get('message')
  type = request.form.get('type')
  date_send = datetime.datetime.now()
  message_user = Chatbot_message_user(id_user = id_user, date_send = date_send, content = content, type = type)

  try:
      db.session.add(message_user)
      db.session.commit()
      data = {'message': 'message inserted', 'code': 'SUCCESS'}
      return make_response(jsonify(data), 201)
  except Exception as e:
      data = {'message': e, 'code': 'ERROR'}
      return make_response(jsonify(data), 500)


@app.route("/get_all_messages",  methods=['POST'])
def get_all_messages():
  id_user = request.form.get('userID')

  try:
    messages = db.session.query(Chatbot_message_user).filter_by(id_user=id_user).order_by(Chatbot_message_user.date_send.asc())
    messages_list = []
    for message in messages:
      message = message.toJSON()
      messages_list.append(message)
    data = {'message': messages_list, 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

  except:
      data = {'message': 'Erreur lors de la recup des messages', 'code': 'ERROR'}
      return make_response(jsonify(data), 500)


@app.route("/get_comparison", methods=['POST'])
def get_comparison():
  try:
    id_user = request.form.get('userID')
    print(str(id_user))
    cur = conn.cursor()
    cur.execute('SELECT date_create FROM of_similarity_test_result WHERE id_user = '+ str(id_user))
    result = cur.fetchall()
    now = datetime.datetime.now()

    if not result:
      data = {'message': get_games_to_compare(id_user), 'code': 'SUCCESS'}
      return make_response(jsonify(data), 201)
    elif (days_between(result[0][0], now) >= -5):
      data = {'message': get_games_to_compare(id_user), 'code': 'SUCCESS'}
      return make_response(jsonify(data), 201)
    else:
      data = {'message': 0, 'code': 'SUCCESS'}
      return make_response(jsonify(data), 201)

  except Exception as e:
    data = {'message': e, 'code': 'ERROR'}
    return make_response(jsonify(data), 500)



@app.route("/index.html")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()