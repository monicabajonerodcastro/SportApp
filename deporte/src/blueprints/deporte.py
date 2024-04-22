from flask import Blueprint, jsonify, request
from src.modelos.database import db_session
from src.comandos.crear_entrenamiento import CrearEntrenamiento
from src.comandos.obtener_entrenamientos import ObtenerEntrenamientos

deporte_blueprint = Blueprint('deporte', __name__, url_prefix="/deporte")

#####################################################################
#                          Health Check                             #
#####################################################################

@deporte_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({"description":"UP"}),200  

#####################################################################
#                          Crear entrenamiento                      #
#####################################################################

@deporte_blueprint.route('/entrenamiento', methods = ['POST'])
def crear_entrenamiento():
    return CrearEntrenamiento(session=db_session,  headers=request.headers,json_request=request.get_json()).execute()

#####################################################################
#                         Paises/Ciudades                           #
#####################################################################

@deporte_blueprint.route("/entrenamientos", methods = ['GET'])
def obtener_entrenamientos():
    return ObtenerEntrenamientos(session=db_session, headers=request.headers).execute()