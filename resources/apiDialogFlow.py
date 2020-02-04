from flask_restful import Resource
from flask import request, jsonify, make_response, g
import status
from sqlalchemy.exc import SQLAlchemyError
import commons
from app import db
import sys
import dialogflow_v2
import os


from controllers import preventaCTL

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
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/datascience/chatbot-cima/credentials/credentials_google_preventa_prod.json"
        session = client.session_path('cima-preventa-aenikt', hash(documento))
        query_input = {"text": {"text": mensaje,"language_code": "Spanish — es"}}

        response = client.detect_intent(session, query_input)

        return make_response(jsonify(
            {
                'mensaje' : response.query_result.fulfillment_text,
                'mensajes' : [response.query_result.fulfillment_text]
            }
        ))