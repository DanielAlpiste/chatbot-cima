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
	msg = ''
	msgs = []

	if (result is not None):
		msg = '¡Felicitaciones! Cuentas con una oferta de hasta S/.' + str(round(result['oferta_maxima'])) + ' . Ingresa a https://cima.pe/login para realizar tu desembolso'

	else:
		result = db.engine.execute(query_preaprobado.replace('$RUC',ruc)).first()
		#si tiene una oferta preaprobada
		if (result is not None):
			#si ya tiene una cuenta 
			usuario = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
			if (usuario is not None):
				msg = '¡¡Felicidades¡¡ Tienes un crédito esperando por ti. Ingresa a: https://cima.pe/login, para que puedas ver las condiciones y aceptar tu oferta. '
			else:
				msg = '¡¡Felicidades¡¡ Tienes un crédito esperando por ti. Ingresa tus datos en: https://cima.pe/credito-pos, para que puedas ver las condiciones y aceptar tu oferta.'
				
		else:
			#si no tiene ninguna oferta
			msg = 'Por ahora no cuentas con una oferta vigente; sin embargo agradecemos el interés y te invitamos a revisar la información dentro de los próximos 30 días, ya que el sistema volverá a evaluarte  de forma automática según tus últimos flujos de venta con VISA.'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def ofertaMasDetalle(ruc):
	query_aprobado = "SELECT bs.document_number AS 'nro_documento', clo.period_in_months AS 'numero_cuotas_maxima', clo.withholding AS 'porcentaje_retencion', clo.base_interest_rate AS 'tasa_interes', clo.monthly_fee AS 'cuota_mensual_maxima',clo.maximum_capital_amount AS 'oferta_maxima' ,a.email FROM business bs JOIN catalog ca ON bs.id = ca.business_id JOIN catalog_item ci ON ca.id = ci.catalog_id JOIN offer clo  ON ci.id = clo.catalog_item_id JOIN account_business ab on ab.business_id = bs.id JOIN account a on a.id = ab.account_id WHERE bs.document_number = '$RUC' AND clo.status ='OFFERED' ORDER BY clo.created_date ASC LIMIT 1"
	query_preaprobado = "SELECT ruc AS 'nro_documento', business_name AS 'razon_social',suitable AS 'pre_califica', final_rate AS 'tasa_interes' FROM ibk_data WHERE ruc = '$RUC';"
	query_registrado = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '$RUC'"

	msgs = []
	
	#si tiene una oferta aprobada
	result = db.engine.execute(query_aprobado.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Para verificar tu oferta ten en cuenta los siguientes pasos: Primero ingresa a CIMA https://cima.pe/login con tu correo: ' + usuario['email'] + '(sin espacios al final) y contraseña con los cuales te registrarste y completa los datos solicitados (*)Si tienes problemas, intenta cerrando tu navegador e ingresando nuevamente'

	else:
		result = db.engine.execute(query_preaprobado.replace('$RUC',ruc)).first()
		#si tiene una oferta preaprobada
		if (result is not None):
			#si ya tiene una cuenta 
			usuario = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
			if (usuario is not None):
				msg = 'Para verificar tu oferta ten en cuenta los siguientes pasos: Primero ingresa a CIMA https://cima.pe/login con tu correo: ' + usuario['email'] + '(sin espacios al final) y contraseña con los cuales te registraste y completa los datos solicitados (*)Si tienes problemas, intenta cerrando tu navegador e ingresando nuevamente'
				#msgs = [
				#	'Primero ingresa a CIMA https://cima.pe/login con tu correo: ' + usuario['email'] + '(sin espacios al final) y contraseña con los cuales te registraste y completa los datos solicitados'
				#	'Luego en la sección de oferta puedes agregar '
				#]
			else:
				msg = 'Al parecer aun no te has registrado en CIMA con tu RUC: ' + ruc + '. Por favor ingresa a https://cima.pe/credito-pos, completa tus datos y dale clic al boton "VER OFERTA" que está al final del formulario para comenzar'
				#msgs = [
				#	'Al parecer aun no te has registrado en CIMA con tu RUC: ' + ruc,
				#	'Primero ingresa a: <a href="https://cima.pe/credito-pos">https://cima.pe/credito-pos</a>',
				#	'Luego en el formulario completa tus datos: RUC, Email (sin espacios en blanco al final), Telefono, Contraseña y Check de VISA',
				#	'Finalmente da clic al boton "VER OFERTA" que se encuentra debajo del formulario'
				#]
		else:
			#si no tiene ninguna oferta
			msg = 'Lo sentimos. Te invitamos a revisar la información dentro de los próximos 30 días, ya que el sistema volverá a evaluarte  de forma automática según tus últimos flujos de venta con VISA.'
	
	d = {}
	d['fulfillmentMessages'] = [{"text": { "text" : msgs}}]
	d['fulfillmentText'] = msg
	return d

def problemaInscripcion(ruc):
	query_registrado = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Recuerda ingresar correctamente tu correo: ' + result['email'] + ' (sin espacios en blanco al final) desde el siguiente link: https://cima.pe/login. En caso no recuerdes tu contraseña deberás darle click a este link para que la puedas restaurar: https://cima.pe/forgot-password'
	else:
		msg = 'Al parecer no estas registrado en CIMA con tu RUC: ' + ruc + ' . Por favor ingresa a https://cima.pe/credito-pos, completa tus datos y dale clic al boton "VER OFERTA" que está al final del formulario para comenzar '
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def problemaLogin(ruc):
	query_registrado = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Recuerda ingresar correctamente tu correo: '+ result['email'] +'(sin espacios al final). En caso no recuerdes tu contraseña deberás darle clic a este link para que la puedas restaurar: https://cima.pe/forgot-password'
	else:
		msg = 'Al parecer no estas registrado en CIMA con tu RUC: ' + ruc + ' . Por favor ingresa a https://cima.pe/credito-pos, completa tus datos y dale clic a "VER OFERTA" para comenzar '
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def problemaLoginError(ruc):
	query_registrado = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',a.email FROM business b JOIN account_business ab on ab.business_id = b.id JOIN account a on a.id = ab.account_id JOIN user u on a.user_id = u.id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_registrado.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Revisa nuevamente que tu correo: '+ result['email'] +' no tenga espacios al final. Este es el link para recuperar tu contraseña: https://cima.pe/forgot-password, Recuerda que se te enviará un email a tu correo electrónico registrado, mediante el cual podrás realizar el cambio de contraseña. De no recibirlo en la bandeja de entrada, revisar la de no deseados (Toda esto deberá realizarce dentro de los 45 minutos desde que recibiste el correo).'
	else:
		msg = 'Al parecer sigues sin estar registrado en CIMA con tu RUC: ' + ruc + ' . Por favor ingresa correctamente tus datos en https://cima.pe/credito-pos y dale clic al boton "VER OFERTA" para continuar'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def getEjecutiva(ruc):
	query_ejecutiva = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',e.first_name AS 'nombre_ejecutiva',e.last_name AS 'apellido_ejecutiva',e.phone  AS 'telefono' FROM business b LEFT JOIN user_business ub on b.id = ub.business_id and ub.type_code = 'EXECUTIVE' LEFT JOIN user e on e.id = ub.user_id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_ejecutiva.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Puedes comunicarte con tu ejecutivo(a) ' + result['nombre_ejecutiva'].capitalize() + ' ' + result['apellido_ejecutiva'] + ' a este número: ' + result['telefono']
	else:
		msg = 'Puedes registrarte en https://cima.pe/credito-pos para luego comunicarte con la ejecutiva que se te asignará.'
	
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
		msg = 'Para cualquier consulta o duda podrás comunicarte con tu ejecutiva ' + result['nombre_ejecutiva'].capitalize() + ' ' + result['apellido_ejecutiva'] + ' a este número: ' + result['telefono'] + '. Recuerda que nuestro horario de atención es de L-V de 9am a 6pm'
	else:
		msg = 'Para cualquier consulta o duda podrás comunicarte al siguiente buzón: cima.interbank@intercorp.com.pe'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def getEjecutivaAyuda(ruc):
	query_ejecutiva = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',e.first_name AS 'nombre_ejecutiva',e.last_name AS 'apellido_ejecutiva',e.phone  AS 'telefono' FROM business b LEFT JOIN user_business ub on b.id = ub.business_id and ub.type_code = 'EXECUTIVE' LEFT JOIN user e on e.id = ub.user_id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_ejecutiva.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = '¡Entendido! En breves momentos tu ejecutiva ' + result['nombre_ejecutiva'].capitalize() + ' ' + result['apellido_ejecutiva'] + ' se comunicará contigo para ayudarte con tu problema. Recuerda que nuestro horario de atención es de L a V de 9am a 6pm'
	else:
		msg = '¡Entendido! En breves momentos nos comunicaremos contigo para ayudarte con tu problema. Recuerda que nuestro horario de atención es de L a V de 9am a 6pm'
	
	d = {}
	d['fulfillmentText'] = msg
	return d

def problemaProceso(ruc):
	query_ejecutiva = "SELECT b.document_type AS 'tipo_documento',b.document_number AS 'nro_documento',e.first_name AS 'nombre_ejecutiva',e.last_name AS 'apellido_ejecutiva',e.phone  AS 'telefono' FROM business b LEFT JOIN user_business ub on b.id = ub.business_id and ub.type_code = 'EXECUTIVE' LEFT JOIN user e on e.id = ub.user_id WHERE document_number = '$RUC'"

	result = db.engine.execute(query_ejecutiva.replace('$RUC',ruc)).first()
	if (result is not None):
		msg = 'Puedes intentar completar el proceso desde una PC o Laptop. ' + 'Para cualquier consulta o duda podrás comunicarte con tu ejecutiva ' + result['nombre_ejecutiva'] + ' ' + result['apellido_ejecutiva'] + ' a este número: ' + result['telefono']
	else:
		msg = 'Puedes intentar completar el proceso desde una PC o Laptop. Si el problema persistiera podrás comunicarte al siguiente buzón: cima.interbank@intercorp.com.pe '
	
	d = {}
	d['fulfillmentText'] = msg
	return d