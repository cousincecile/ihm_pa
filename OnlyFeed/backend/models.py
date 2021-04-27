from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()
engine = create_engine('postgresql:///onlyfeed', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# define your models classes hereafter
class Opinion(Base):
	__tablename__ = 'opinion'

	id = db.Column(db.Integer, primary_key=True)
	id_user = db.Column(db.Integer)
	date_pub = db.Column(db.DateTime)
	comment = db.Column(db.Text)
	id_vg = db.Column(db.Integer)
	rate = db.Column(db.Float)

	def toJSON(self):       
		json = {
			"id":self.id,
			"id_user":self.id_user,
			"date_pub":self.date_pub,
			"comment":self.comment,
			"id_vg":self.id_vg,
			"rate":self.rate     
		}

		return json