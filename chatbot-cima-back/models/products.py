from app import db, ma
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from marshmallow import Schema, fields
from marshmallow_validators.wtforms import from_wtforms
from wtforms.validators import Email, Length
from sqlalchemy import *

class Products(db.Model):
	__tablename__='products'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column('NAME', db.String(100), unique=True)
	prize = db.Column('PRIZE', db.Float)

	@classmethod
	def addOne(self,obj):
		db.session.add(obj)
		db.session.commit()
		db.session.flush()
		return obj.id