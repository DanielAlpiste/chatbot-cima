import status
from app import db

from models.cima_loan_calendar import CIMA_Loan_Calendar

def returnPrize(nameOfFlower):
	prize = Products.query.filter(Products.name == nameOfFlower).first().prize
	str = 'Una ' + nameOfFlower + ' cuesta: S/.' + "{:.2f}".format(prize) + '. Desea alguna?'
	d = {}
	d['fulfillmentText'] = str
	d['prize'] = prize
	return d

def returPrizeCant(cantidad, nameOfFlower):
	prize = Products.query.filter(Products.name == nameOfFlower).first().prize
	prizeTot = cantidad * prize
	str = 'Eso te estaria costando: S/.' + "{:.2f}".format(prizeTot) + '. Va a querer? Porque esto pesa como mrd'
	d = {}
	d['fulfillmentText'] = str
	d['prize'] = prizeTot
	return d

