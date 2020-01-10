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

		if(action == 'action-numero-documento'):
			ruc = d.get('queryResult').get('outputContexts')[0].get('parameters').get('doc_number.original')
			resp = preventaCTL.verificarNumeroDocumento(ruc)
		
		#if (action == 'action-verificar-email'):

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