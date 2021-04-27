from flask import Flask
from models import db, Base, Opinion
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS, cross_origin
from pprint import pprint
from inspect import getmembers


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
db.init_app(app)
db = SQLAlchemy(app)
data = []



def index():
    data = test_data()
    return render_template("index.html",result = data)

def test_data():
    sss = db.session.query(Opinion).get(1).id_user
    return sss

@app.route("/index")
def main():
    return index()

if __name__ == '__main__':
    app.run()