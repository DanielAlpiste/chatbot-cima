from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_filename):
	app = Flask(__name__)
	app.config.from_object(config_filename)
	
	db.init_app(app)
	ma.init_app(app)
	
	from views import api_bp
	app.register_blueprint(api_bp, url_prefix='/api')

	return app
