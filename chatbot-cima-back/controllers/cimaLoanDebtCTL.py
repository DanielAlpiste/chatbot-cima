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
		cuotasVencidas = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.credit_code == numCredito, CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.payment_date < datetime.datetime.now()).subquery()
		listaCuotasVencidas = db.session.query(CIMA_Loan_Debt).join(cuotasVencidas, cuotasVencidas.c.quota_order == CIMA_Loan_Debt.quota_order).filter(CIMA_Loan_Debt.credit_code == numCredito).order_by(CIMA_Loan_Debt.quota_order.asc()).all()
		msg = ''
		if(len(listaCuotasVencidas) != 0):
			msg += 'Tienes ' + str(len(listaCuotasVencidas)) + ' cuotas vencidas.\n'
			for i in listaCuotasVencidas:
				falta = i.amount - i.total_partial_paid
				msg += 'De la cuota numero ' + str(i.quota_order) + ' has pagado S/. ' + "{:.2f}".format(i.total_partial_paid) + '. Y te faltan S/. ' + "{:.2f}".format(falta) + '.\n'
		sigCuota = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.credit_code == numCredito, CIMA_Loan_Calendar.document_number == numDocumento, CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.payment_date > datetime.datetime.now()).order_by(CIMA_Loan_Calendar.quota_order.asc()).first()
		if sigCuota is not None:
			sigCuota = sigCuota.quota_order
			cuotaAct = CIMA_Loan_Debt.query.filter(CIMA_Loan_Debt.credit_code == numCredito, CIMA_Loan_Debt.quota_order == sigCuota).first()
			faltaAct = cuotaAct.amount - cuotaAct.total_partial_paid
			msg += 'De tu actual cuota, has pagado S/. ' + "{:.2f}".format(cuotaAct.total_partial_paid) + '. Y te faltan S/. ' + "{:.2f}".format(faltaAct) + '.\n:D.'
		d = {}
		d['fulfillmentText'] = msg
		return d