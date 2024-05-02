from flask import Blueprint, jsonify, request
from src.comandos.calcular_indicadores import CalcularIndicadores
from src.comandos.registrar_sesion_entrenamiento import FinalizarSesionEntrenamiento, IniciarSesionEntrenamiento
from src.comandos.remover_plan_deportista import RemoverPlanDeportista
from src.comandos.obtener_plan_por_deportista import ObtenerPlanesDeportista
from src.comandos.asignar_plan_deportista import AsignarPlanDeportista
from src.comandos.obtener_entrenamientos_plan import ObtenerEntrenamientosPlan
from src.comandos.obtener_deporte_por_id import ObtenerDeportePorId
from src.comandos.obtener_deportes import ObtenerDeportes
from src.comandos.enviar_productos_rutina_alimenticia import EnviarProductosRutinaAlimenticia
from src.comandos.asociar_producto_a_rutina import AsociarProductoARutina
from src.comandos.crear_producto_alimenticio import CrearProductoAlimenticio
from src.comandos.crear_rutina_alimenticia import CrearRutinaAlimenticia
from src.modelos.database import db_session
from src.comandos.crear_entrenamiento import CrearEntrenamiento
from src.comandos.obtener_entrenamientos import ObtenerEntrenamientos
from src.comandos.crear_plan_entrenamiento import CrearPlanEntrenamiento
from src.comandos.obtener_planes_entrenamiento import ObtenerPlanesEntrenamiento

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

#####################################################################
#                             Deportes                              #
#####################################################################

@deporte_blueprint.route("/deportes", methods = ['GET'])
def obtener_deportes():
    return ObtenerDeportes(session=db_session).execute()


@deporte_blueprint.route("/deportes/<string:id_deporte>", methods = ['GET'])
def obtener_deporte_por_id(id_deporte):
    return ObtenerDeportePorId(session=db_session, id_deporte=id_deporte).execute()

#####################################################################
#                       Planes de entrenamiento                     #
#####################################################################

@deporte_blueprint.route("/planes-entrenamiento", methods = ['GET'])
def obtener_plan_entrenamiento():
    return ObtenerPlanesEntrenamiento(session=db_session, headers=request.headers).execute()

@deporte_blueprint.route("/planes-entrenamiento/<string:id_plan>", methods = ['GET'])
def obtener_entrenamientos_plan(id_plan):
    return ObtenerEntrenamientosPlan(session=db_session, id_plan=id_plan, headers=request.headers).execute()

@deporte_blueprint.route('/plan-entrenamiento', methods = ['POST'])
def crear_plan_entrenamiento():
    return CrearPlanEntrenamiento(session=db_session, headers=request.headers, json_request=request.get_json()).execute()

@deporte_blueprint.route("/planes-entrenamiento/<string:id_plan>/deportista", methods = ["POST"])
def asignar_plan_deportista(id_plan):
    return AsignarPlanDeportista(session=db_session, headers=request.headers, id_plan=id_plan).execute()

@deporte_blueprint.route("/planes-entrenamiento/<string:id_plan>/deportista", methods = ["DELETE"])
def remover_plan_deportista(id_plan):
    return RemoverPlanDeportista(session=db_session, headers=request.headers, id_plan=id_plan).execute()

@deporte_blueprint.route("/planes-entrenamiento/deportista", methods = ["GET"])
def obtener_plan_deportista():
    return ObtenerPlanesDeportista(session=db_session, headers=request.headers).execute()

#####################################################################
#                       Sesion de entrenamiento                     #
#####################################################################

@deporte_blueprint.route('/sesion-entrenamiento/iniciar', methods = ['POST'])
def iniciar_sesion_entrenamiento():
    return IniciarSesionEntrenamiento(session=db_session, headers=request.headers).execute()

@deporte_blueprint.route('/sesion-entrenamiento/finalizar', methods = ['POST'])
def finalizar_sesion_entrenamiento():
    return FinalizarSesionEntrenamiento(session=db_session, headers=request.headers, json_request=request.get_json()).execute()

#####################################################################
#                             Indicadores                           #
#####################################################################

@deporte_blueprint.route("/indicadores", methods = ["GET"])
def obtener_indicadores():
    return CalcularIndicadores(session=db_session, headers=request.headers).execute()