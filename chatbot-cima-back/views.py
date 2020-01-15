from flask import Blueprint
from flask_restful import Api, Resource


# *********** Models *********** #
#from models.cima_enterprise import CIMA_Enterprise
#from models.cima_loan_calendar import CIMA_Loan_Calendar
#from models.cima_loan_debt import CIMA_Loan_Debt

# *********** Resources *********** #
from resources import webhookRSC

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(webhookRSC.Consult, '/webhook')
