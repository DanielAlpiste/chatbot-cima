from app import db
from sqlalchemy import *

class ChatbotConversation(db.Model):
	__bind_key__ = 'datascience'
	__tablename__='ibk_chatbot_history'
	id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
	conversacion = db.Column('CONVERSATION_ID', db.String(100))
	documento = db.Column('DOCUMENTO', db.String(11))
	fecha = db.Column('FECHA', db.DateTime)
	pregunta = db.Column('PREGUNTA', db.String(500))
	intencion = db.Column('INTENCION', db.String(25))
	respuesta = db.Column('RESPUESTA', db.String(500))

	@classmethod
	def addOne(self,obj):
		db.session.add(obj)
		db.session.commit()
		db.session.flush()
		return obj.id