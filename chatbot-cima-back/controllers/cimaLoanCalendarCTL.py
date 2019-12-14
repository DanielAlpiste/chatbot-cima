import status
from app import db
import commons

from models.cima_loan_calendar import CIMA_Loan_Calendar
from models.cima_enterprise import CIMA_Enterprise

def consultPayDay(tipoDocumento, numDocumento, numCuota):
	if tipoDocumento=='dni':
		numDocumento = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first().ruc
	
	if(type(numCuota) == list):
		if(numCuota[0] == 'max'):
			dia_de_pago = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.document_number == numDocumento).order_by(CIMA_Loan_Calendar.disburse_date.desc(), CIMA_Loan_Calendar.payment_date.desc()).first()
		if(numCuota[0] == 'sig'):
			dia_de_pago = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.document_number == numDocumento).order_by(CIMA_Loan_Calendar.disburse_date.desc(), CIMA_Loan_Calendar.payment_date.asc()).first()
		else:
			dia_de_pago = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.quota_order == numCuota[0], CIMA_Loan_Calendar.document_number == numDocumento).order_by(CIMA_Loan_Calendar.disburse_date.desc()).first()
		
	if(dia_de_pago is None):
		str = 'Esa cuota no existe :( Quizá te has equivocado.'
	else:
		dia_de_pago = dia_de_pago.payment_date
		dia_de_pago = commons.convertDatetime(dia_de_pago)
		str = 'La fecha de pago para esta cuota es el dia ' + dia_de_pago + ' :D'
	
	d = {}
	d['fulfillmentText'] = str
	return d

def consultPayCalendar(tipoDocumento, numDocumento):
	if tipoDocumento=='dni':
		numDocumento = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first().ruc
	listaCuotas = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.document_number == numDocumento).order_by(CIMA_Loan_Calendar.quota_order.asc()).all()
	if listaCuotas is None:
		msg = '¡No tienes ninguna deuda pendiente! Genial :D'
	else:
		msg = 'Esta es la informacion sobre tus siguientes cuotas:\n'
		for i in listaCuotas:
			msg += 'En la cuota número ' + str(i.quota_order) + ' debes pagar S./ ' + "{:.2f}".format(i.amount) + '. Esta la deberias cancelar el dia ' +  commons.convertDatetime(i.payment_date) + '.\n'
		msg += ':D'
	d = {}
	d['fulfillmentText'] = msg
	return d

def consultQuota(tipoDocumento, numDocumento):
	if tipoDocumento=='dni':
		numDocumento = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first().ruc
	sigCuota = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.document_number == numDocumento).order_by(CIMA_Loan_Calendar.payment_date.asc()).first()
	if sigCuota is None:
		msg = '¡No tienes ninguna cuota pendiente! Genial :D'
	else:
		msg = 'El valor de la cuota solicitada es de S./ ' + "{:.2f}".format(sigCuota.amount) + ' :D'
	d = {}
	d['fulfillmentText'] = msg
	return d

def consultPrecancel(tipoDocumento, numDocumento):
	if tipoDocumento=='dni':
		numDocumento = CIMA_Enterprise.query.filter(CIMA_Enterprise.client_dni == numDocumento).first().ruc
	cuotasFaltantes = CIMA_Loan_Calendar.query.filter(CIMA_Loan_Calendar.status == 'PENDING', CIMA_Loan_Calendar.document_number == numDocumento).order_by(CIMA_Loan_Calendar.payment_date.asc()).all()
	if(len(cuotasFaltantes)==1):
		msg = 'Veo en el sistema que esta es tu última cuota :D ¡Eso quiere decir que puedes precancelarla y verificar si calificas para un nuevo crédito directamente desde nuestra web! Ingresa a www.cima.pe de inmediato para que puedas realizar este proceso :D'
	else:
		msg = 'Pues esta no es tu última cuota. Eso quiere decir que, si quieres precancelar, tienes que acercarte a tu tienda Interbank más cercana y decir que quieres adelantar el pago de la operación número ' + str(cuotasFaltantes[0].credit_code) + ' :)'
	d = {}
	d['fulfillmentText'] = msg
	return d