from flask import Blueprint
from flask_restful import Api, Resource


# *********** Models *********** #
from models.intents import Intents
from models.products import Products

# *********** Resources *********** #
from resources import webhookRSC

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(webhookRSC.Consult, '/webhook')
