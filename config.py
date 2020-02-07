import os


# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
PORT = 8080
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_DATABASE_URI = "postgres://mxljwstnibggum:65800360c274e407ff75a9ae30bce95376102a3f27bf50d5f71165c73354a847@ec2-107-20-168-237.compute-1.amazonaws.com:5432/d2m21pplhiqetl"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
PAGINATION_PAGE_SIZE = 5
#PAGINATION_PAGE_ARGUMENT_NAME = 'page'
#SECRET_KEY = 'loconfieso'
"""
"""

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario_consulta:nBw4mT3bpTsXUb2W@35.226.45.124:3306/cima_prod_db'
SQLALCHEMY_BINDS = {
    #'datascience': 'mysql+pymysql://chatbot:9KwKSRCq2be74WhPWTRq@108.59.81.200:3306/ibk-data-science'
    'datascience': 'mysql+pymysql://diego:Febrero2020@localhost:3306/cima'
}

#SQLALCHEMY_POOL_SIZE = 5
#SQLALCHEMY_POOL_TIMEOUT = 30
#SQLALCHEMY_POOL_RECYCLE = 31
#SQLALCHEMY_TRACK_MODIFICATIONS  = False


#DIALOGFLOW_CREDENTIALS = '/home/datascience/chatbot-cima/credentials/credentials_google_preventa_prod.json'
#DIALOGFLOW_PROJECT = 'cima-preventa-aenikt'

DIALOGFLOW_CREDENTIALS = 'C:\\Users\\B34300\\Desktop\\chatbot_app\\aceleraton\\produccion\\chatbot-cima-pre\\credentials\\credentials_google_preventa_pre.json'
DIALOGFLOW_PROJECT = 'preventa-test-vbmamn'

MAIL_URL = 'https://api.sendgrid.com/v3/mail/send'
MAIL_TOKEN = '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'
MAIL_RECEIPT = 'dlopezp@intercorp.com.pe'