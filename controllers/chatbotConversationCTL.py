import status
from app import db
from datetime import datetime

from models.chatbotConversation import ChatbotConversation

def insert(conversation_id,documento,pregunta,intencion,respuesta):

	obj = ChatbotConversation(
		conversacion = conversation_id,
		documento = documento,
		fecha = datetime.now(),
		pregunta = pregunta,
		intencion = intencion,
		respuesta = respuesta
	)
	id = ChatbotConversation.addOne(obj)
	return id
