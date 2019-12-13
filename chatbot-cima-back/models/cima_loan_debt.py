from app import db, ma
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from wtforms.validators import Email, Length
from sqlalchemy import *

class CIMA_Loan_Debt(db.Model):
	__tablename__='cima_loan_debt'
	document_type = db.Column(db.String(10), primary_key=True)
	document_number = db.Column(db.String(50), primary_key=True)
	credit_code = db.Column(db.String(50), primary_key=True)
	quota_order = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Float)
	days_expired = db.Column(db.Integer)
	expired_debt_interest = db.Column(db.Float)
	compensatory_interest = db.Column(db.Float)
	collection_penalty = db.Column(db.Float)
	total_partial_paid = db.Column(db.Float)
	total_debt = db.Column(db.Float)
	
	@classmethod
	def addOne(self,obj):
		db.session.add(obj)
		db.session.commit()
		db.session.flush()
		return obj.ruc