import status
from app import db
import datetime

from models.cima_loan_debt import CIMA_Loan_Debt 
from models.cima_loan_calendar import CIMA_Loan_Calendar
from models.cima_enterprise import CIMA_Enterprise

def consultPaidAndNotPaid(tipoDocumento, numDocumento):
	if tipoDocumento=='dni':
		numDocumento = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first().ruc
	
	numCredito = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING').order_by(CIMA_Loan_Calendar.payment_date.desc()).first()
	if(numCredito is None):
		msg = '¡No tienes ninguna deuda pendiente! Genial :D'
		d = {}
		d['fulfillmentText'] = msg
		return d
	else:
		numCredito = numCredito.credit_code
		cuotasPagadas = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.credit_code == numCredito, CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PAID').subquery()
		listaCuotasPagadas = db.session.query(CIMA_Loan_Debt).join(cuotasPagadas, cuotasPagadas.c.quota_order == CIMA_Loan_Debt.quota_order).filter(CIMA_Loan_Debt.credit_code == numCredito).order_by(CIMA_Loan_Debt.quota_order.asc()).all()
		msg = ''
		if(len(listaCuotasPagadas) != 0):
			msg += 'Haz pagado ya ' + str(len(listaCuotasPagadas)) + ' cuotas :)\n'
			for i in listaCuotasPagadas:
				falta = i.amount - i.total_partial_paid
				msg += 'De la cuota numero ' + str(i.quota_order) + ' has pagado S/. ' + "{:.2f}".format(i.amount) + '.\n'
		cuotasVencidas = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.credit_code == numCredito, CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.payment_date < datetime.datetime.now()).subquery()
		listaCuotasVencidas = db.session.query(CIMA_Loan_Debt).join(cuotasVencidas, cuotasVencidas.c.quota_order == CIMA_Loan_Debt.quota_order).filter(CIMA_Loan_Debt.credit_code == numCredito).order_by(CIMA_Loan_Debt.quota_order.asc()).all()
		if(len(listaCuotasVencidas) != 0):
			msg += 'Tienes ' + str(len(listaCuotasVencidas)) + ' cuotas vencidas.\n'
			for i in listaCuotasVencidas:
				falta = i.amount - i.total_partial_paid
				msg += 'De la cuota numero ' + str(i.quota_order) + ' ya has recaudado S/. ' + "{:.2f}".format(i.total_partial_paid) + '. Y te falta recaudar S/. ' + "{:.2f}".format(falta) + '.\n'
		sigCuota = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.credit_code == numCredito, CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.payment_date > datetime.datetime.now()).order_by(CIMA_Loan_Calendar.quota_order.asc()).first()
		if sigCuota is not None:
			sigCuota = sigCuota.quota_order
			cuotaAct = CIMA_Loan_Debt.query.filter(CIMA_Loan_Debt.credit_code == numCredito, CIMA_Loan_Debt.quota_order == sigCuota).first()
			faltaAct = cuotaAct.amount - cuotaAct.total_partial_paid
			msg += 'De tu actual cuota, ya has recaudado S/. ' + "{:.2f}".format(cuotaAct.total_partial_paid) + '. Y te falta recaudar S/. ' + "{:.2f}".format(faltaAct) + '.\n'
		msg+= 'Este es tu estado de cuenta actual registrado en nuestro sistema :D'
		d = {}
		d['fulfillmentText'] = msg
		return d

def consultSMSIssue(tipoDocumento, numDocumento):
	if tipoDocumento=='dni':
		numDocumento = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first().ruc
	
	numCredito = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.payment_date < datetime.datetime.now()).order_by(CIMA_Loan_Calendar.payment_date.desc()).first()
	if(numCredito is None):
		msg = '¡No tienes ninguna deuda pendiente! Es muy raro que se te haya enviado ese mensaje. En todo caso comunicate con mi amiga, la Ejecutiva de Negocios CIMA, Ross :P Su numero es: 967769873.'
		d = {}
		d['fulfillmentText'] = msg
		return d
	else:
		numCredito = numCredito.credit_code
		cuotasVencidas = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.credit_code == numCredito, CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.payment_date < datetime.datetime.now()).subquery()
		listaCuotasVencidas = db.session.query(CIMA_Loan_Debt).join(cuotasVencidas, cuotasVencidas.c.quota_order == CIMA_Loan_Debt.quota_order).filter(CIMA_Loan_Debt.credit_code == numCredito).order_by(CIMA_Loan_Debt.quota_order.asc()).all()
		msg = 'Pues tienes ' + str(len(listaCuotasVencidas))
		if(len(listaCuotasVencidas) > 1):
			msg += ' cuotas vencidas :('
		else:
			msg += ' cuota vencida :('
		msg += ' Sucede que aqui en CIMA enviamos mensajes de texto cada vez que nuestros clientes tienen una o mas deudas vencidas. Si la informacion que te acabo de decir es erronea, comunicate con mi amiga, la Ejecutiva de Negocios CIMA, Ross :P Su numero es: 967769873.'
		d = {}
		d['fulfillmentText'] = msg
		return d

def saldoConocer(tipoDocumento, numDocumento):
	if tipoDocumento=='dni':
		numDocumento = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first().ruc
	numCredito = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.payment_date < datetime.datetime.now()).order_by(CIMA_Loan_Calendar.payment_date.desc()).first()
	if(numCredito is None):
		msg = '¡No tienes ninguna deuda pendiente! Eso es genial :D'
		d = {}
		d['fulfillmentText'] = msg
		return d
	numCredito = numCredito.credit_code	
	cuotasTotales = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.credit_code == numCredito).order_by(CIMA_Loan_Calendar.payment_date.asc()).all()
	tasa = cuotasTotales[0].interest_rate
	pagado = 0
	faltante = 0
	for i in cuotasTotales:
		if(i.status == 'PAID'):
			pagado += i.amount
		elif(i.status == 'PENDING'):
			faltante += i.amount

	cuotasFaltantes = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.credit_code == numCredito, CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING').subquery()
	listaCuotasFaltantes = db.session.query(CIMA_Loan_Debt).join(cuotasFaltantes, cuotasFaltantes.c.quota_order == CIMA_Loan_Debt.quota_order).filter(CIMA_Loan_Debt.credit_code == numCredito).order_by(CIMA_Loan_Debt.quota_order.asc()).all()
	
	recaudado = 0
	faltaRecaudar = 0
	for i in listaCuotasFaltantes:
		recaudado += i.total_partial_paid
		faltaRecaudar += i.amount - i.total_partial_paid
	
	msg = 'Muy bien. Tu credito tiene las siguientes caracteristicas:\nTu tasa es de ' + "{:.2f}".format(tasa) + '%.\n'
	msg += 'Lo pagado de tu deuda es S/. ' + "{:.2f}".format(pagado) + ', y te faltan S/. ' + "{:.2f}".format(faltante) + '.\n'
	msg += 'Por ultimo, de lo faltante, has logrado recaudar S./ ' + "{:.2f}".format(recaudado) + ', y te falta recaudar S/. ' + "{:.2f}".format(faltaRecaudar) + '.\n :D'
	d = {}
	d['fulfillmentText'] = msg
	return d