import status
from app import db

from models.products import Products

def jsonifyProduct(obj):
	d = {}
	d['id'] = obj.id
	d['name'] = obj.name
	d['prize'] = obj.prize
	return d

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
	str = 'Eso te estaria costando: S/.' + "{:.2f}".format(prizeTot) + '. '
	d = {}
	d['fulfillmentText'] = str
	d['prize'] = prizeTot
	return d

