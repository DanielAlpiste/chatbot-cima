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

		if(d.get('queryResult').get('outputContexts')[0].get('parameters').get('documento.original') is None):
			if(action=='action-saludo'):
				resp['fulfillmentMessages'] = d.get('queryResult').get('fulfillmentMessages')
				resp['fulfillmentMessages'][0]['text']['text'] = ['Hola! somos CIMA','Para poder comenzar necesitamos tu numero de documento']
			else:
				resp['fulfillmentText'] = 'Para poder comenzar necesitamos tu numero de documento'

		else:
			if(action=='action-documento'):
				resp['fulfillmentText'] = 'Muy bien! Ahora cuentanos en que podemos ayudarte'
				resp['outputContexts'] = d.get('queryResult').get('outputContexts')
				resp['outputContexts'][0].get('parameters')['nombre'] = 'Diego'



		#######################################################################################
		if(action == 'action-numero-documento'):
			ruc = d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original')
			resp = preventaCTL.verificarNumeroDocumento(ruc)

		if(action == 'action-oferta'):
			ruc = d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original')
			resp = preventaCTL.verificarOferta(ruc)

		if(action=='action-problema-inscripcion'):
			ruc = d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original')
			resp = preventaCTL.problemaInscripcion(ruc)

		if(action=='action-problema-login'):
			ruc = d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original')
			resp = preventaCTL.problemaLogin(ruc)

		if(action=='action-numero-telefonico'):
			ruc = d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original')
			resp = preventaCTL.getEjecutiva(ruc)

		return  make_response(jsonify(resp))