import status
from app import db

def verificarNumeroDocumento(ruc):

	persona = None
	query = "SELECT business_name as 'razon_social', client_first_name as 'nombre', final_rate as 'tasa' FROM ibk_data where ruc = '$RUC'"
	result = db.engine.execute(query.replace('$RUC',ruc)).first()
	if result is not None:
		persona = result
	return persona

def verificarOferta(ruc):
	query_aprobado = "SELECT bs.document_number AS 'nro_documento', clo.period_in_months AS 'numero_cuotas_maxima', clo.withholding AS 'porcentaje_retencion', clo.base_interest_rate AS 'tasa_interes', clo.monthly_fee AS 'cuota_mensual_maxima',clo.maximum_capital_amount AS 'oferta_maxima' FROM business bs JOIN catalog ca ON bs.id = ca.business_id JOIN catalog_item ci ON ca.id = ci.catalog_id JOIN offer clo  ON ci.id = clo.catalog_item_id WHERE bs.document_number = '$RUC' AND clo.status ='OFFERED' ORDER BY clo.created_date ASC LIMIT 1"
	query_preaprobado = "SELECT ruc AS 'nro_documento', business_name AS 'razon_social',suitable AS 'pre_califica', final_rate AS 'tasa_interes' FROM ibk_data WHERE ruc = '$RUC';"
	query_registrado = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '$RUC'"

	#si tiene una oferta aprobada
	result = db.engine.execute(query_aprobado.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = '¡Felicitaciones! Cuentas con una oferta de hasta S/.' + str(round(result['oferta_maxima'])) + ' . Ingresa a https://cima.pe/login para realizar tu desembolso'

	else:
		result = db.engine.execute(query_preaprobado.replace('$RUC',ruc)).first()
		#si tiene una oferta preaprobada
		if (result is not None):
			#si ya tiene una cuenta 
			usuario = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
			if (usuario is not None):
				msg = '¡¡Felicidades¡¡ Tienes un crédito esperando por ti. Ingresa a https://cima.pe/login con tu cuenta para que puedas aceptar la oferta para que podamos proceder con tu desembolso'
			else:
				msg = '¡¡Felicidades¡¡ Tienes un crédito esperando por ti. Ingresa a Cima: https://cima.pe/credito-pos, regístrate y completa los pasos. El sistema te evaluará en línea y te mostrará las condiciones de tu crédito. De estar de acuerdo deberás aceptar la oferta para que podamos proceder con tu desembolso.'
		else:
			#si no tiene ninguna oferta
			msg = 'Por ahora no cuentas con una oferta vigente; sin embargo agradecemos el interés y te invitamos a revisar la información dentro de los próximos 30 días, ya que el sistema volverá a evaluarte  de forma automática según tus últimos flujos de venta con VISA.'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def problemaInscripcion(ruc):
	query_registrado = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Recuerda ingresar correctamente tu correo: ' + result['email'] + ' (sin espacios) desde el siguiente link: https://cima.pe/login. En caso no recuerdes tu contraseña deberás darle click a este link para que la puedas restaurar: https://cima.pe/forgot-password'
	else:
		msg = 'Al parecer no estas ingresando con el correo registrado en CIMA (' + result['email'] +'). Revisa que este sea el correo correcto (sin espacios). Caso contrario puedes registrarte desde https://cima.pe/credito-pos'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def problemaLogin(ruc):
	query_registrado = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Recuerda ingresar correctamente tu correo: '+ result['email'] +'. En caso no recuerdes tu contraseña deberás darle clic a este link para que la puedas restaurar: https://cima.pe/forgot-password'
	else:
		msg = 'Al parecer no estas ingresando con el correo registrado en CIMA. Revisa que tu correo sea correcto (sin espacios). Caso contrario puedes registrarte desde https://cima.pe/credito-pos'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def getEjecutiva(ruc):
	query_ejecutiva = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',e.first_name AS 'nombre_ejecutiva',e.last_name AS 'apellido_ejecutiva',e.phone  AS 'telefono' FROM business b LEFT JOIN user_business ub on b.id = ub.business_id and ub.type_code = 'EXECUTIVE' LEFT JOIN user e on e.id = ub.user_id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_ejecutiva.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Puedes comunicarte con tu ejecutivo(a) ' + result['nombre_ejecutiva'].capitalize() + ' ' + result['apellido_ejecutiva'] + ' a este número: ' + result['telefono']
	else:
		msg = 'Hola, la comunicación es por este medio. Si necesitas mas información primero regístrate en https://cima.pe/credito-pos para comunicarte con uno de nuestros ejecutivos'
	
	d = {}
	d['fulfillmentText'] = msg
	return d
	
def getEjecutivaSoporte(ruc):
	query_ejecutiva = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',e.first_name AS 'nombre_ejecutiva',e.last_name AS 'apellido_ejecutiva',e.phone  AS 'telefono' FROM business b LEFT JOIN user_business ub on b.id = ub.business_id and ub.type_code = 'EXECUTIVE' LEFT JOIN user e on e.id = ub.user_id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_ejecutiva.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Parece que no logro entender lo que quieres decir. Puedes comunicarte con tu ejecutivo(a) ' + result['nombre_ejecutiva'].capitalize() + ' ' + result['apellido_ejecutiva'] + ' a este número: ' + result['telefono']
	else:
		msg = 'Parece que no logro entender lo que quieres decir. Un ejecutivo de negocio se comunicara a tu numero telefónico.'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def getEjecutiva(ruc):
	query_ejecutiva = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',e.first_name AS 'nombre_ejecutiva',e.last_name AS 'apellido_ejecutiva',e.phone  AS 'telefono' FROM business b LEFT JOIN user_business ub on b.id = ub.business_id and ub.type_code = 'EXECUTIVE' LEFT JOIN user e on e.id = ub.user_id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_ejecutiva.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Para cualquier consulta o duda podrás comunicarte con tu ejecutiva ' + result['nombre_ejecutiva'].capitalize() + ' ' + result['apellido_ejecutiva'] + ' a este número: ' + result['telefono']
	else:
		msg = 'Para cualquier consulta o duda podrás comunicarte al siguiente buzón: cima.interbank@intercorp.com.pe '
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def problemaProceso(ruc):
	query_ejecutiva = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',e.first_name AS 'nombre_ejecutiva',e.last_name AS 'apellido_ejecutiva',e.phone  AS 'telefono' FROM business b LEFT JOIN user_business ub on b.id = ub.business_id and ub.type_code = 'EXECUTIVE' LEFT JOIN user e on e.id = ub.user_id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_ejecutiva.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Puedes intentar completar el proceso desde una PC o Laptop. Puedes comunicarte con tu ejecutivo(a) ' + 'Para cualquier consulta o duda podrás comunicarte con tu ejecutiva ' + result['nombre_ejecutiva'] + ' ' + result['apellido_ejecutiva'] + ' a este número: ' + result['telefono']
	else:
		msg = 'Puedes intentar completar el proceso desde una PC o Laptop. Si el problema persistiera podrás comunicarte al siguiente buzón: cima.interbank@intercorp.com.pe '
	
	d = {}
	d['fulfillmentText'] = msg
	return d