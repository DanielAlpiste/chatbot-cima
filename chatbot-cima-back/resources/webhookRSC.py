from flask_restful import Resource
from flask import request, jsonify, make_response, g
import status
from sqlalchemy.exc import SQLAlchemyError

from controllers import cimaEnterpriseCTL

class Consult(Resource):
	def post(self):
		d = request.get_json(force=True)
		action = d.get('queryResult').get('action')
		if not d:
			response = {'user': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		
		if(action == 'validacion_documento'):
			tipoDocumento = d.get('queryResult').get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('parameters').get('numero_documento')
			msg = cimaEnterpriseCTL.validateDocument(tipoDocumento, numDocumento)
		return  make_response(jsonify(msg))
		#
		#
		#elif(action == 'decision_cantidad'):
		#	cantidad = d.get('queryResult').get('parameters').get('cantidad')
		#	nameOfFlower = d.get('queryResult').get('outputContexts')[0].get('parameters').get('flor_consulta_precio')
		#	msg = productsCTL.returPrizeCant(cantidad, nameOfFlower)
		#return