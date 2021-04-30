from flask import Flask
from models import db, Base, Chatbot_User
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS, cross_origin



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
    #data = add_data()
    return render_template("index.html",result = data)


def first_connection():
    return render_template("first_connection.html")


@app.route("/first_connection.html", methods =["POST"])
def add_data():
    if request.method == "POST":
           # getting input with name = fname in HTML form
        username = request.form.get("fusername")
        email = request.form.get("femail") 
        age = request.form.get("fage")
        user1 = Chatbot_User(username= username, email= email, age= age)
        db.session.add(user1)
        db.session.commit()
        sss = db.session.query(Chatbot_User).get(2).id
    return render_template("index.html")


@app.route("/first_connection.html")
def main():
    return first_connection()

if __name__ == '__main__':
    app.run()