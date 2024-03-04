from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

import os 
from flask import Flask, jsonify
from .blueprints.alerta import alertas_blueprint
from .errors.errors import ApiError

app = Flask(__name__)

app.register_blueprint(alertas_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code

    
