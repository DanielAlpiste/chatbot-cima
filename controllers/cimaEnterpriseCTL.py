import status
from app import db

from models.cima_enterprise import CIMA_Enterprise

def validateDocument(tipoDocumento, numDocumento):
	if(tipoDocumento == 'dni'):
		persona = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first()
	elif(tipoDocumento == 'ruc'):
		persona = CIMA_Enterprise.query.filter(CIMA_Enterprise.ruc == numDocumento).first()
	
	if(persona is None):
		str = 'Lamentablemente no eres un cliente nuestro :( Si te interesa saber si tenemos un crédito para ti, puedes ingresar a www.cima.pe :D'
	else:
		str = '¡Hola ' + persona.client_first_name + '! Parece que eres tú pero aún no estoy muy segura :( ¿Podrías decirme la dirección de correo electrónico con la que te registraste a CIMA?'
	
	d = {}
	d['fulfillmentText'] = str
	return d

def validateEmail(tipoDocumento, numDocumento):
	if(tipoDocumento == 'dni'):
		persona = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first()
	elif(tipoDocumento == 'ruc'):
		persona = CIMA_Enterprise.query.filter(CIMA_Enterprise.ruc == numDocumento).first()
	str = '¡Si eras tú ' + persona.client_first_name + '! :) Que bueno tenerte de vuelta por este chat. ¿En qué puedo ayudarte?'
	d = {}
	d['fulfillmentText'] = str
	return d