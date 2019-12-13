from flask_restful import Resource
from flask import request, jsonify, make_response, g
import status
from sqlalchemy.exc import SQLAlchemyError

from controllers import productsCTL

class Consult(Resource):
	def post(self):
		d = request.get_json(force=True)
		if not d:
			response = {'user': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		
		action = d.get('queryResult').get('action')
		if(action == 'consultar_precio'):
			msg = productsCTL.returnPrize(d.get('queryResult').get('parameters').get('flor_consulta_precio'))
		elif(action == 'decision_cantidad'):
			cantidad = d.get('queryResult').get('parameters').get('cantidad')
			nameOfFlower = d.get('queryResult').get('outputContexts')[0].get('parameters').get('flor_consulta_precio')
			msg = productsCTL.returPrizeCant(cantidad, nameOfFlower)
		return make_response(jsonify(msg))