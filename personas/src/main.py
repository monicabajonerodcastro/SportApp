from dotenv import load_dotenv
loaded = load_dotenv('.env.prod')

import os 
from flask import Flask, jsonify
from .blueprints.personas import personas_blueprint
from .blueprints.swagger import swagger_ui_blueprint
from .errors.errors import ApiError
from .models.database import Base, engine
from sqlalchemy import inspect

SWAGGER_URL="/swagger"

app = Flask(__name__)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(personas_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code

    
def init_db():
  Base.metadata.create_all(bind=engine)
    
with app.app_context():
  init_db()

