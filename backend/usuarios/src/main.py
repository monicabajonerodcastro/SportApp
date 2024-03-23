from flask import Flask
from .blueprints.usuarios import usuarios_blueprint

app = Flask(__name__)

app.register_blueprint(usuarios_blueprint)
