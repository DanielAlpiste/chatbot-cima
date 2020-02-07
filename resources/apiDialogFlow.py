from flask_restful import Resource
from flask import request, jsonify, make_response, g
from flask import current_app
import status
from sqlalchemy.exc import SQLAlchemyError
import commons
from app import db
import sys
import dialogflow_v2
import os

from controllers import preventaCTL
from controllers import chatbotConversationCTL

class Send(Resource):
    
    def post(self):

        mensaje = request.form.get('mensaje')
        documento = request.form.get('documento')

        if not mensaje:
            response = {'mensaje': 'no se envio mensaje'}
            return response, status.HTTP_400_BAD_REQUEST
        
        if not documento:
            response = {'documento': 'no se envio documento'}
            return response, status.HTTP_400_BAD_REQUEST
        
        client = dialogflow_v2.SessionsClient()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = current_app.config['DIALOGFLOW_CREDENTIALS']
        session = client.session_path(current_app.config['DIALOGFLOW_PROJECT'], hash(documento))
        query_input = {"text": {"text": mensaje,"language_code": "Spanish — es"}}

        response = client.detect_intent(session, query_input)

        msgs = []
        for m in response.query_result.fulfillment_messages[0].text.text:
            msgs.append(m)
        
        if len(msgs) < 1:
            msgs.append(response.query_result.fulfillment_text)

        return make_response(jsonify(
            {
                'mensaje' : response.query_result.fulfillment_text,
                'mensajes' : msgs
            }
        ))