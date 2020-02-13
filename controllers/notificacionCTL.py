import status
import requests
from app import db
from flask import current_app
from datetime import datetime,timedelta
import json

from models.chatbotConversation import ChatbotConversation

def enviar(conversacion,ruc,accion):

    if accion == 'input.unknown':
        body = '<p>El bot no pudo reconocer la siguiente conversación con el cliente ' + ruc +'</p>'
    elif accion in ['action-post-estado-cuota','action-post-estado-retencion']:
        body = '<p>El cliente requiere información sobre sus retenciones/cuotas:  ' + ruc + '</p>'
    elif accion == 'action-error-contacto-ejecutivo':
        body = '<p>El cliente no pudo completar su tarea:  ' + ruc + '</p>'

    conversa = ChatbotConversation.query.filter(ChatbotConversation.conversacion == conversacion). \
            filter(ChatbotConversation.fecha >= (datetime.now() - timedelta(minutes=15))) .\
            all()
    
    for c in conversa:
        body += '<br><b>Cliente: </b>' + c.pregunta
        body += '<br><b>CIMA: </b>' + c.respuesta


    data = {}
    data['personalizations'] = [{'to': [{"email": current_app.config['MAIL_RECEIPT']}]}]
    data['from'] = {"email": "chatbot@cima.pe"}
    data['subject'] = "Chatbot Cima  - Conversación"
    data['content'] = [{"type": "text/html","value": body}]

    hed = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + current_app.config['MAIL_TOKEN']
        }

    result = requests.post(current_app.config['MAIL_URL'],headers=hed,data=json.dumps(data))

    return result