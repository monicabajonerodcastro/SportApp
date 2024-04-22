from flask import Blueprint, jsonify, request
from src.comandos.enviar_productos_rutina_alimenticia import EnviarProductosRutinaAlimenticia
from src.comandos.asociar_producto_a_rutina import AsociarProductoARutina
from src.comandos.crear_producto_alimenticio import CrearProductoAlimenticio
from src.comandos.crear_rutina_alimenticia import CrearRutinaAlimenticia
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
#                         Lista entrenamientos                      #
#####################################################################

@deporte_blueprint.route("/entrenamientos", methods = ['GET'])
def obtener_entrenamientos():
    return ObtenerEntrenamientos(session=db_session, headers=request.headers).execute()


#####################################################################
#                       Productos alimenticios                      #
#####################################################################

@deporte_blueprint.route('/producto-alimenticio', methods = ["POST"])
def crear_producto_alimenticio():
    return CrearProductoAlimenticio(session=db_session, headers=request.headers, json_request=request.get_json()).execute()

#####################################################################
#                         Rutinas alimenticias                      #
#####################################################################

@deporte_blueprint.route('/rutina-alimenticia', methods = ['POST'])
def crear_rutina_alimenticia():
    return CrearRutinaAlimenticia(session=db_session, headers=request.headers, json_request=request.get_json()).execute()

@deporte_blueprint.route('/rutina-alimenticia/<string:id_rutina_alimenticia>/producto-alimenticio', methods=['POST'])
def asociar_producto_a_rutina(id_rutina_alimenticia):
    return AsociarProductoARutina(session=db_session, headers=request.headers, id_rutina_alimenticia=id_rutina_alimenticia, json_request=request.get_json()).execute()

@deporte_blueprint.route('/rutina-alimenticia/<string:id_rutina_alimenticia>/enviar', methods = ["POST"])
def enviar_productos_alimenticios(id_rutina_alimenticia):
    return EnviarProductosRutinaAlimenticia(session=db_session, headers=request.headers, id_rutina_alimenticia=id_rutina_alimenticia).execute()

