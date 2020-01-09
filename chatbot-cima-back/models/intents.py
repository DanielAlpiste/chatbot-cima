from app import db
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import *

class Intents(db.Model):
	__tablename__='intents'
	id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
	num_doc = db.Column('NUM_DOC', db.String(30), unique=True)
	context = db.Column('CONTEXT', db.String(500))

	@classmethod
	def addOne(self,obj):
		db.session.add(obj)
		db.session.commit()
		db.session.flush()
		return obj.id