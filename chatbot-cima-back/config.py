import os


# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
PORT = 9994
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

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://acelerathon-cima:KGKMHfM388baAGFUcFv8@108.59.81.200:3306/acelerathon_cima'
#SQLALCHEMY_POOL_SIZE = 5
#SQLALCHEMY_POOL_TIMEOUT = 30
#SQLALCHEMY_POOL_RECYCLE = 31
#SQLALCHEMY_TRACK_MODIFICATIONS  = False
