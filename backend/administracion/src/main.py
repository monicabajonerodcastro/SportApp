from dotenv import load_dotenv
loaded = load_dotenv('.env.environment')

import os
from flask import Flask, jsonify
from .errores.errores import ApiError
from .blueprints.administracion import administracion_blueprint
from .modelos.database import Base, engine
from sqlalchemy import inspect

app = Flask(__name__)

app.register_blueprint(administracion_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code

    
def init_db():
  if not inspect(engine).has_table("usuarios"):
    Base.metadata.create_all(bind=engine)
    
with app.app_context():
  init_db()