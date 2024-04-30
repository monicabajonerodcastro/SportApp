from dotenv import load_dotenv
loaded = load_dotenv('.env.prod')

import os
from flask import Flask, jsonify
from flask_cors import CORS
from .errores.errores import ApiError
from .blueprints.administracion import administracion_blueprint
from .blueprints.swagger import swagger_ui_blueprint
from .modelos.database import Base, engine, db_session

SWAGGER_URL="/swagger"

app = Flask(__name__)
CORS(app)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(administracion_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "description": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code

@app.teardown_request
def session_clear(exception=None):
    db_session.remove()
    if exception and db_session.is_active:
        db_session.rollback()
    
def init_db():
  Base.metadata.create_all(bind=engine)
    
with app.app_context():
  init_db()