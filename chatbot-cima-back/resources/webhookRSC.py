from flask_restful import Resource
from flask import request, jsonify, make_response, g
import status
from sqlalchemy.exc import SQLAlchemyError
import commons
from app import db

from controllers import preventaCTL

class Consult(Resource):
	def post(self):
		d = request.get_json(force=True)
		if not d:
			response = {'user': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		
		action = d.get('queryResult').get('action')
		resp = {}
		ruc = ''
		telefono = ''


		#validacion de datos RUC y TELEFONO
		if (action == 'input.unknown'):
			if (d.get('queryResult').get('outputContexts')[0].get('parameters') is None):
				resp['fulfillmentText'] = 'El RUC/DNI que has ingresado no esta en formato correcto, recuerda que deben ser 11 u 8 dígitos. ¿Puedes ingresarlo nuevamente?'
				return resp
			if (d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original') is None):
				resp['fulfillmentText'] = 'El teléfono que has ingresado no esta en formato correcto, recuerda que deben ser 9 dígitos. ¿Puedes ingresarlo nuevamente?'
				return resp
		
		#si no se reconoce la intencion por segunda vez
		if (action == 'input.unknown.2'):
			if (d.get('queryResult').get('outputContexts')[0].get('parameters') is None):
				resp['fulfillmentText'] = 'Parece que no logro entender lo que quieres decir. Un ejecutivo de negocio se comunicara a tu numero telefónico.'
				return resp
			if (d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original') is not None):
				resp = preventaCTL.getEjecutiva(d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original'))


		#Si no ha ingresado el numero de documento
		if(d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original') is None):
			#si me saluda, respondo el saludo y le pido el documento
			if(action=='action-saludo'):
				resp['fulfillmentText'] = "Hola, Bienvenido a CIMA soy tu asistente virtual que te ayudará a obtener tu préstamo rápido y fácil. \u000A Para poder comenzar necesitamos primero tu RUC o DNI"
				resp['fulfillmentMessages'] = d.get('queryResult').get('fulfillmentMessages')
				resp['fulfillmentMessages'][0]['text']['text'] = ['Hola, Bienvenido a CIMA soy tu asistente virtual que te ayudará a obtener tu préstamo rápido y fácil.','Para poder comenzar necesitamos primero tu RUC o DNI']
			#para el resto de intenciones pido el documento
			else:
				resp['fulfillmentText'] = '¡Hola!. Antes de continuar necesitamos primero tu RUC o DNI'
		else:
			#Si esta el documento pero no el telefono
			ruc = d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original')

			if(d.get('queryResult').get('outputContexts')[0].get('parameters').get('telefono.original') is None):
				resp['fulfillmentText'] = 'Para darte una mejor atención también bríndanos tu número telefónico'
			else:
				#si ya estan seteado ambos despues de llenarlos, pongo frase de pregunta y seteo nombres
				if(action in ['action-numero-documento','action-telefono']):
					resp['fulfillmentText'] = '¡Entendido! Ahora cuéntanos ¿En que podemos ayudarte?'
					persona = preventaCTL.verificarNumeroDocumento(ruc)
					if persona is not None:
						resp['outputContexts'] = d.get('queryResult').get('outputContexts')
						resp['outputContexts'][0].get('parameters')['nombre'] = persona['nombre'].capitalize()
						resp['outputContexts'][0].get('parameters')['razon_social'] = persona['razon_social'].title()
						resp['outputContexts'][0].get('parameters')['tasa'] = persona['tasa']

				#si ya estan seteados ambos, proceso como normalmente lo haria
				else:
					
					if(action == 'action-oferta'):
						resp = preventaCTL.verificarOferta(ruc)

					if(action=='action-problema-inscripcion'):
						resp = preventaCTL.problemaInscripcion(ruc)

					if(action=='action-problema-login'):
						resp = preventaCTL.problemaLogin(ruc)

					if(action=='action-numero-telefonico'):
						resp = preventaCTL.getEjecutiva(ruc)

					if(action=='action-problema-proceso'):
						resp = preventaCTL.problemaProceso(ruc)
						

		#######################################################################################		

		return  make_response(jsonify(resp))