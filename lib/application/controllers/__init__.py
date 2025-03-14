from flask import Flask
from lib.application.controllers.VehiculeController import vehicule_bp
from lib.application.controllers.ContratController import contrat_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'

    app.register_blueprint(vehicule_bp, url_prefix='/api')
    app.register_blueprint(contrat_bp, url_prefix='/api')

    return app