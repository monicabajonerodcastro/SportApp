from flask import Flask
from .blueprints.alertas import alertas_blueprint

app = Flask(__name__)

app.register_blueprint(alertas_blueprint)
