from app import db, ma
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from marshmallow import Schema, fields
from marshmallow_validators.wtforms import from_wtforms
from wtforms.validators import Email, Length
from sqlalchemy import *

class CIMA_Enterprise(db.Model):
	__tablename__='cima_enterprise'
	ruc = db.Column(db.String(30), primary_key=True, unique = True)
	business_name = db.Column(db.String(500))
	suitable = db.Column(db.Float)
	final_rate = db.Column(db.Float)
	client_dni = db.Column(db.String(30))
	client_first_name = db.Column(db.String(255))
	client_last_name = db.Column(db.String(255))
	sbs_clasification = db.Column(db.String(10))
	max_pd = db.Column(db.Float)
	company_type = db.Column(db.Integer)

	@classmethod
	def addOne(self,obj):
		db.session.add(obj)
		db.session.commit()
		db.session.flush()
		return obj.ruc