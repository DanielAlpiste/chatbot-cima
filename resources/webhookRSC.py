from flask_restful import Resource
from flask import request, jsonify, make_response, g
import status
from sqlalchemy.exc import SQLAlchemyError
import commons
from app import db
import sys

from controllers import preventaCTL
from controllers import chatbotConversationCTL
from controllers import notificacionCTL

class Consult(Resource):

	def getContexto(self,contextos):
		c = None
		for context in contextos:
			url = context.get('name').split('/')
			if url[-1] == 'datos-personales':
				c = context
		return c

	def post(self):


		d = request.get_json(force=True)
		if not d:
			response = {'user': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		
		action = d.get('queryResult').get('action')
		contexto = self.getContexto(d.get('queryResult').get('outputContexts'))

		conversacion = d.get('session')
		intencion = d.get('queryResult').get('intent').get('displayName')
		pregunta = d.get('queryResult').get('queryText')

		resp = {}
		resp['fulfillmentText'] = d.get('queryResult').get('fulfillmentText')
		ruc = ''
		telefono = ''
		notificar = False

		#Si no reconoce ninguna intencion
		if (action == 'input.unknown'):

			#No hay RUC por lo tanto no lo ingresó correctamente
			if (contexto is None or contexto.get('parameters') is None or contexto.get('parameters').get('doc_number.original') is None):
				resp['fulfillmentText'] = 'El RUC que has ingresado no esta en formato correcto, recuerda que deben ser 11. ¿Puedes ingresarlo nuevamente?'
			#No hay Telefono por lo tanto no lo ingreso correctamente
			elif (contexto.get('parameters').get('telefono.original') is None):
				resp['fulfillmentText'] = 'El teléfono que has ingresado no esta en formato correcto, recuerda que deben ser 9 dígitos. ¿Puedes ingresarlo nuevamente?'
			
			#Tiene los datos de RUC y Telefono pero no reconocio intención (contador 1)
			elif (contexto.get('parameters').get('error') is None):
				ruc = contexto.get('parameters').get('doc_number.original')
				resp['outputContexts'] = [contexto]
				resp['outputContexts'][0].get('parameters')['error'] = 1
				resp['fulfillmentText'] = 'Creo que no entendí tu consulta, ¿Puedes decirla de otra manera?'

			#Tiene los datos de RUC y Telefono pero no reconocio intención (contador 2)
			elif(contexto.get('parameters')['error'] == 1):
				ruc = contexto.get('parameters').get('doc_number.original')
				resp['fulfillmentText'] = 'Lo sentimos parece que no podemos resolver tu duda por este medio. Una ejecutiva de negocio se estará comunicando contigo a tu telefono en la brevedad posible'
				notificar = True

		#si hay alguna intencion reconocida
		else:
			#si me saluda 
			if(action=='action-saludo'):

				#pero no hay documento
				if contexto is None or contexto.get('parameters').get('doc_number.original') is None:
					resp['fulfillmentText'] = "Hola, Bienvenido a CIMA soy tu asistente virtual que te ayudará a obtener tu préstamo rápido y fácil. \u000A Para poder comenzar necesitamos primero tu RUC"

				#si no hay telefono
				elif contexto.get('parameters').get('telefono.original') is None:
					resp['fulfillmentText'] = 'Para darte una mejor atención también bríndanos tu número telefónico'
				
				else:
					resp['fulfillmentText'] = 'Hola ¿En qué podemos ayudarte?'
				
			#si ha ingreso su documento o telefono
			elif(action in ['action-numero-documento','action-telefono']):

				#pero no hay documento
				if contexto is None or contexto.get('parameters').get('doc_number.original') is None:
					resp['fulfillmentText'] = "Para poder comenzar primero necesitamos primero tu RUC"

				#si no hay telefono
				elif contexto.get('parameters').get('telefono.original') is None:
					resp['fulfillmentText'] = 'Para darte una mejor atención también bríndanos tu número telefónico'
				
				#si ya ingreso correctamente ambos datos
				else:
					resp['fulfillmentText'] = '¡Entendido! Ahora cuéntanos ¿En que podemos ayudarte?'
					ruc = contexto.get('parameters').get('doc_number.original')
					persona = preventaCTL.verificarNumeroDocumento(ruc)
					if persona is not None:
						resp['outputContexts'] = [contexto]
						resp['outputContexts'][0].get('parameters')['nombre'] = persona['nombre'].capitalize()
						resp['outputContexts'][0].get('parameters')['razon_social'] = persona['razon_social'].title()
						resp['outputContexts'][0].get('parameters')['tasa'] = persona['tasa']

			#si ya estan seteados ambos, proceso como normalmente lo haria
			else:

				#pero no hay documento
				if contexto is None or contexto.get('parameters').get('doc_number.original') is None:
					resp['fulfillmentText'] = "Para poder comenzar primero necesitamos primero tu RUC"

				#si no hay telefono
				elif contexto.get('parameters').get('telefono.original') is None:
					resp['fulfillmentText'] = 'Para darte una mejor atención también bríndanos tu número telefónico'
				
				#Si todo va en orden
				else:
					ruc = contexto.get('parameters').get('doc_number.original')

					if(action == 'action-oferta'):
						resp = preventaCTL.verificarOferta(ruc)

					if(action=='action-problema-inscripcion'):
						resp = preventaCTL.problemaInscripcion(ruc)

					if(action=='action-problema-login'):
						resp = preventaCTL.problemaLogin(ruc)

					if(action=='action-numero-telefonico'):
						resp = preventaCTL.getEjecutiva(ruc)

					if(action=='action-problema-proceso'):
						resp = preventaCTL.problemaProceso(ruc)

					if (action=='action-error-contacto-ejecutivo'):
						resp = preventaCTL.getEjecutivaAyuda(ruc)
						notificar = True

					if (action=='action-oferta-mas-detalle'):
						resp = preventaCTL.ofertaMasDetalle(ruc)
					
					if (action=='action-problema-login-error1'):
						resp = preventaCTL.problemaLoginError(ruc)

					if (action in ['action-post-estado-cuota','action-post-estado-retencion']):
						notificar = True


						

		#######################################################################################		
		#Guardando conversacion en Base de Datos
		
		respuesta = resp['fulfillmentText']
		chatbotConversationCTL.insert(conversacion,ruc,pregunta,intencion,respuesta)
		if notificar:
			notificacionCTL.enviar(conversacion,ruc,action)

		return make_response(jsonify(resp))