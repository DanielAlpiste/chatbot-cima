from flask_restful import Resource
from flask import request, jsonify, make_response, g
import status
from sqlalchemy.exc import SQLAlchemyError

from controllers import cimaEnterpriseCTL
from controllers import cimaLoanCalendarCTL
from controllers import cimaLoanDebtCTL

class Consult(Resource):
	def post(self):
		d = request.get_json(force=True)
		if not d:
			response = {'user': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST

		action = d.get('queryResult').get('action')

		if(action == 'validacion_documento'):
			tipoDocumento = d.get('queryResult').get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('parameters').get('numero_documento')
			msg = cimaEnterpriseCTL.validateDocument(tipoDocumento, numDocumento)
		
		elif(action == 'validacion_correo'):
			tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
			msg = cimaEnterpriseCTL.validateEmail(tipoDocumento, numDocumento)
		
		elif(action == 'conocer_fecha_pago'):
			numCuota = d.get('queryResult').get('parameters').get('cuota_orden')
			tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
			msg = cimaLoanCalendarCTL.consultPayDay(tipoDocumento, numDocumento, numCuota)

		elif(action == 'obtener_cronograma'):
			tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
			msg = cimaLoanCalendarCTL.consultPayCalendar(tipoDocumento, numDocumento)

		elif(action == 'conocer_valor_cuota'):
			tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
			msg = cimaLoanCalendarCTL.consultQuota(tipoDocumento, numDocumento)

		elif(action == 'obtener_recaudacion_y_faltante'):
			tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
			msg = cimaLoanDebtCTL.consultPaidAndNotPaid(tipoDocumento, numDocumento)

		elif(action == 'conocer_motivo_SMS'):
			tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
			numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
			msg = cimaLoanDebtCTL.consultSMSIssue(tipoDocumento, numDocumento)
		return  make_response(jsonify(msg))
		#
		#elif(action == 'decision_cantidad'):
		#	cantidad = d.get('queryResult').get('parameters').get('cantidad')
		#	nameOfFlower = d.get('queryResult').get('outputContexts')[0].get('parameters').get('flor_consulta_precio')
		#	msg = productsCTL.returPrizeCant(cantidad, nameOfFlower)
		#return