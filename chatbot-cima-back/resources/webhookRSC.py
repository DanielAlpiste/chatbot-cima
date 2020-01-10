from flask_restful import Resource
from flask import request, jsonify, make_response, g
import status
from sqlalchemy.exc import SQLAlchemyError
import commons
from app import db

from controllers import cimaEnterpriseCTL
from controllers import cimaLoanCalendarCTL
from controllers import cimaLoanDebtCTL

class Consult(Resource):
	def post(self):
		d = request.get_json(force=True)
		if not d:
			response = {'user': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST

		ruc = ''
		telefono = ''
		msg = ''
		
		action = d.get('queryResult').get('action')

		if(action == 'action-oferta'):
			query_aprobado = "SELECT bs.document_number AS 'nro_documento', clo.period_in_months AS 'numero_cuotas_maxima', clo.withholding AS 'porcentaje_retencion', clo.base_interest_rate AS 'tasa_interes', clo.monthly_fee AS 'cuota_mensual_maxima',clo.maximum_capital_amount AS 'oferta_maxima' FROM business bs JOIN catalog ca ON bs.id = ca.business_id JOIN catalog_item ci ON ca.id = ci.catalog_id JOIN offer clo  ON ci.id = clo.catalog_item_id WHERE bs.document_number = '$RUC' AND clo.status ='OFFERED' ORDER BY clo.created_date ASC LIMIT 1"
			query_preaprobado = "SELECT ruc AS 'nro_documento', business_name AS 'razon_social',suitable AS 'pre_califica', final_rate AS 'tasa_interes' FROM ibk_data WHERE ruc = '$RUC';"

			#si tiene una oferta aprobada
			result = db.engine.execute(query_aprobado.replace('$RUC',documento))
			if (len(result) > 0):
				msg = 'Cuentas con una oferta de hasta S/.' + result[0]['maximum_capital_amount']
			else if:
				result = db.engine.execute(query_preaprobado.replace('$RUC',documento))
				#si tiene una oferta preaprobada
				if (len(result) > 0):
					msg = 'Cuentas con una oferta preaprobada, ingresa/registrate a cima para verla'
				else:
					#si no tiene ninguna oferta
					msg = 'Actualmente no cuentas con una oferta'
				
		if(action == ''):

		if(action == ''):
			
			#msg = cimaEnterpriseCTL.validateDocument(tipoDocumento, numDocumento)
		
		#elif(action == 'validacion_correo'):
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaEnterpriseCTL.validateEmail(tipoDocumento, numDocumento)
		#
		#elif(action == 'conocer_fecha_pago'):
		#	numCuota = d.get('queryResult').get('parameters').get('cuota_orden')
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaLoanCalendarCTL.consultPayDay(tipoDocumento, numDocumento, numCuota)
#
		#elif(action == 'obtener_cronograma'):
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaLoanCalendarCTL.consultPayCalendar(tipoDocumento, numDocumento)
#
		#elif(action == 'conocer_valor_cuota'):
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaLoanCalendarCTL.consultQuota(tipoDocumento, numDocumento)
#
		#elif(action == 'obtener_recaudacion_y_faltante'):
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaLoanDebtCTL.consultPaidAndNotPaid(tipoDocumento, numDocumento)
#
		#elif(action == 'conocer_motivo_SMS'):
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaLoanDebtCTL.consultSMSIssue(tipoDocumento, numDocumento)
#
		#elif(action == 'consultar_precancelacion'):
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaLoanCalendarCTL.consultPrecancel(tipoDocumento, numDocumento)
#
		#elif(action == 'conocer_saldo'):
		#	tipoDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('tipo_documento')
		#	numDocumento = d.get('queryResult').get('outputContexts')[0].get('parameters').get('numero_documento.original')
		#	msg = cimaLoanDebtCTL.saldoConocer(tipoDocumento, numDocumento)
		d = {}
		d['fulfillmentText'] = msg
		return  make_response(jsonify(d))
		
		#
		#elif(action == 'decision_cantidad'):
		#	cantidad = d.get('queryResult').get('parameters').get('cantidad')
		#	nameOfFlower = d.get('queryResult').get('outputContexts')[0].get('parameters').get('flor_consulta_precio')
		#	msg = productsCTL.returPrizeCant(cantidad, nameOfFlower)
		#return