import status
from app import db

def verificarNumeroDocumento(documento):
	text = "SELECT b.document_type AS 'tipo_documento', b.document_number AS 'nro_documento', a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '" + documento + "'"
	query = db.engine.execute(text).first()
	if query is None:
		msg = "Usted no es cliente nuestro, quizá se equivoco de RUC, si no es asi, puede comunicarse con uno de nuestros ejecutivos."
	else:
		msg = "¡Perfecto! Ahora, ¿puedes decirme tu correo electronico?"
	d = {}
	d['fulfillmentText'] = msg
	return d

def verificarEmail(documento, email):
	text = "SELECT b.document_type AS 'tipo_documento', b.document_number AS 'nro_documento', a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '" + documento + "' and a.email = '" + email + "'"
	query = db.engine.execute(text).first()
	if query is None:
		msg = "Usted no es cliente nuestro, quizá se equivoco de email, si no es asi, puede comunicarse con uno de nuestros ejecutivos."
	else:
		msg = "¡Excelente! ¿Cuál es su duda el día de hoy?"
	d = {}
	d['fulfillmentText'] = msg
	return d

def verificarOferta(documento):
	query_aprobado = "SELECT bs.document_number AS 'nro_documento', clo.period_in_months AS 'numero_cuotas_maxima', clo.withholding AS 'porcentaje_retencion', clo.base_interest_rate AS 'tasa_interes', clo.monthly_fee AS 'cuota_mensual_maxima',clo.maximum_capital_amount AS 'oferta_maxima' FROM business bs JOIN catalog ca ON bs.id = ca.business_id JOIN catalog_item ci ON ca.id = ci.catalog_id JOIN offer clo  ON ci.id = clo.catalog_item_id WHERE bs.document_number = '$RUC' AND clo.status ='OFFERED' ORDER BY clo.created_date ASC LIMIT 1"
	query_preaprobado = "SELECT ruc AS 'nro_documento', business_name AS 'razon_social',suitable AS 'pre_califica', final_rate AS 'tasa_interes' FROM ibk_data WHERE ruc = '$RUC';"

	#si tiene una oferta aprobada
	result = db.engine.execute(query_aprobado.replace('$RUC',ruc))
	if (len(result) > 0):
		msg = 'Cuentas con una oferta de hasta S/.' + result[0]['maximum_capital_amount']
	else:
		result = db.engine.execute(query_preaprobado.replace('$RUC',ruc))
		#si tiene una oferta preaprobada
		if (len(result) > 0):
			msg = 'Cuentas con una oferta preaprobada, ingresa/registrate a cima para verla'
		else:
			#si no tiene ninguna oferta
			msg = 'Actualmente no cuentas con una oferta'
	
	d = {}
	d['fulfillmentText'] = msg
	return d