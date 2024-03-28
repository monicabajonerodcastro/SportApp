from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

import os 
from flask import Flask, jsonify
from .blueprints.personas import personas_blueprint
from .errors.errors import ApiError
from .models.database import Base, engine
from sqlalchemy import inspect


app = Flask(__name__)

app.register_blueprint(personas_blueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), err.code

    
def init_db():
  if not inspect(engine).has_table("usuario"):
    Base.metadata.create_all(bind=engine)
    
with app.app_context():
  init_db()

