from flask import Flask, jsonify, make_response, render_template, request, redirect
from flask_bootstrap import Bootstrap
from models import db, Base, Chatbot_User, Chatbot_message_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS, cross_origin
import datetime



app = Flask(__name__)
CORS(app)
Bootstrap(app)

POSTGRES = {
    'user': 'root',
    'pw': 'root',
    'db': 'onlyfeed',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)
db = SQLAlchemy(app)
data = []

@app.route("/get_cookies", methods=['POST'])
def get_cookies():
    email = request.cookies.get('email')
    data = {'message': email, 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)


@app.route('/set_cookies', methods = ['POST'])
def setcookie():
   if request.method == 'POST':
       email = request.form['email']
       username = request.form['username']
       
       resp = make_response(render_template('index.html'))
       resp.set_cookie('email', email)
       resp.set_cookie('username', username)
       
       return resp


@app.route("/add_user_message",  methods=['POST'])
def add_user_message():
    id_user = 1
    content = request.form.get('data')
    date_received = datetime.datetime.now()
    message_user = Chatbot_message_user(id_user = id_user, date_received = date_received, content = content)

    try:
        db.session.add(message_user)
        db.session.commit()
        data = {'message': 'message inserted', 'code': 'SUCCESS'}
        return make_response(jsonify(data), 201)
    except:
        data = {'message': 'Erreur lors de l\'insertion', 'code': 'ERROR'}
        return make_response(jsonify(data), 500)

@app.route("/index.html")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()