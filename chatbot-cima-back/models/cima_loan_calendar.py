from app import db
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from wtforms.validators import Email, Length
from sqlalchemy import *

class CIMA_Loan_Calendar(db.Model):
	__tablename__='cima_loan_calendar'
	quota_order = db.Column(db.Integer, primary_key=True)
	credit_code = db.Column(db.String(50), primary_key=True)
	document_type = db.Column(db.String(10), primary_key=True)
	document_number = db.Column(db.String(50), primary_key=True)
	disburse_date = db.Column(db.DateTime)
	payment_date = db.Column(db.DateTime)
	quota_duration_days = db.Column(db.Integer)
	amount = db.Column(db.Float)
	pending_capital = db.Column(db.Float)
	interest = db.Column(db.Float)
	amortization = db.Column(db.Float)
	status = db.Column(db.String(100))
	effective_payment_date = db.Column(db.Date)
	interest_rate = db.Column(db.Float)
	disbursed_amount = db.Column(db.Float)
	
	@classmethod
	def addOne(self,obj):
		db.session.add(obj)
		db.session.commit()
		db.session.flush()
		return obj.ruc