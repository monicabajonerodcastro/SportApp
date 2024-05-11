import datetime
from flask import Blueprint, jsonify, request
from src.errores.errores import InternalServerError
from src.comandos.agregar_entrenamientos_strava import AgregarEntrenamientosStrava
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
from src.comandos.obtener_entrenamientos import ObtenerEntrenamientoPorId, ObtenerEntrenamientos
from src.comandos.crear_plan_entrenamiento import CrearPlanEntrenamiento
from src.comandos.obtener_planes_entrenamiento import ObtenerPlanesEntrenamiento
from src.servicios import http

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

#####################################################################
#                             Strava                           #
#####################################################################

@deporte_blueprint.route("/get-activities/<string:access_token>", methods = ["GET"])
def obtener_actividades(access_token):
    StravaUrlActivities= "https://www.strava.com/api/v3/athlete/activities"
    response=http.get_request(url=StravaUrlActivities, headers={'Authorization': 'Bearer '+access_token})
    if response.status_code < 200 or response.status_code > 209:
        raise InternalServerError(description="Ocurrio un error al obtener las actividades de Strava")
    response=response.json()
    return response
    
@deporte_blueprint.route("/get_strava/<string:access_token>", methods = ["POST"])
def agregar_entrenamientos_strava(access_token):
    activities=obtener_actividades(access_token)
    return AgregarEntrenamientosStrava(session=db_session, headers=request.headers, activities=activities).execute()


@deporte_blueprint.route("/add_activity_strava", methods = ["POST"])
def agregar_entrenamiento_strava():
    
    json_request=request.get_json()
    
    entrenamiento=ObtenerEntrenamientoPorId(session=db_session, id_entrenamiento=json_request["id_entrenamiento"]).execute()
    body = {

        "name": entrenamiento["nombre"],
        "sport_type": "Walk",
        "start_date_local":  datetime.datetime.utcnow().isoformat(),
        "elapsed_time": 0,
        "description": entrenamiento["detalle"]
    }
    
    StravaUrlActivities= "https://www.strava.com/api/v3/activities"
    response=http.post_request(url=StravaUrlActivities, headers={'Authorization': 'Bearer '+ json_request["access_token"]},data=body)
     
    response=response.json()
    
    return response