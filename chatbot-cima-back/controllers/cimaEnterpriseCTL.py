import status
from app import db

from models.cima_enterprise import CIMA_Enterprise

def validateDocument(tipoDocumento, numDocumento):
	#prize = Products.query.filter(Products.name == nameOfFlower).first().prize
	str = 'Que tal senor Daniel Alpiste. Usted si se encuentra pre aprobado para un credito con nosotros. Pero necesitamos validar mas su informacion. Me podria decir su tasa?'
	d = {}
	d['fulfillmentText'] = str
	return d
