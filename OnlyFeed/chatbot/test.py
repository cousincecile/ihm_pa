from flask import Flask, jsonify, make_response, render_template, request, redirect
from models import db, Base, Chatbot_User, Chatbot_message_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS, cross_origin
import datetime
import json

app = Flask(__name__)
CORS(app)

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db = SQLAlchemy(app)

def get_user(username):
	added_user = db.session.query(Chatbot_User).filter_by(username=username).first()
	print(added_user.toJSON())

get_user("test")