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
