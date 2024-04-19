
from flask import Blueprint, jsonify, request
from src.comandos.asignar_reunion_usuario import AsignarReunionUsuario
from src.comandos.crear_reunion import CrearReunion
from src.comandos.obtener_reuniones import ObtenerReuniones, ObteneReunionesDisponibles
from src.comandos.crear_entrenador import CrearEntrenador
from src.comandos.obtener_entrenador import ObtenerEntrenador, ObtenerentrenadorId
from src.comandos.obtener_entrenadores import ObtenerEntrenadores
from src.comandos.actualizar_socio import ActualizarSocio
from src.comandos.obtener_plan_por_id import ObtenerPlanId
from src.comandos.obtener_planes import ObtenerPlan
from src.comandos.asignar_deportista_a_plan import AsignarDeportistaPlan
from src.modelos.database import db_session

from flask import Blueprint, jsonify, request
from src.comandos.crear_socio import CrearSocio
from src.comandos.obtener_socio import ObtenerSocio, ObtenerSocioId
from src.comandos.obtener_socios import ObtenerSocios
from src.comandos.obtener_paises import ObtenerPaises
from src.comandos.obtener_deportes import ObtenerDeportes
from src.comandos.obtener_ciudades import ObtenerCiudades
from src.errores.errores import MissingRequiredField
from src.comandos.crear_producto_servicio import CrearProductoServicio
from src.comandos.obtener_producto_servicios import ObtenerProductoServicios

administracion_blueprint = Blueprint('administracion', __name__, url_prefix="/administracion")

#####################################################################
#                          Health Check                             #
#####################################################################

@administracion_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({"description":"UP"}),200  

#####################################################################
#                              Planes                               #
#####################################################################

@administracion_blueprint.route('/plan', methods = ['GET'])
def obtener_planes():
    return ObtenerPlan(session=db_session, headers=request.headers).execute()

@administracion_blueprint.route('/plan/<string:id_plan>', methods = ['GET'])
def get_plan_por_id(id_plan):
    return ObtenerPlanId(session=db_session, headers=request.headers, id_plan=id_plan).execute()

@administracion_blueprint.route('/plan/deportista', methods=["POST"])
def asignar_deportista_a_plan():
    return AsignarDeportistaPlan(session=db_session, headers=request.headers, json_request=request.get_json()).execute()

#####################################################################
#                             Socios                                #
#####################################################################

@administracion_blueprint.route('/socio', methods = ['POST'])
def crear_socio():
    json_request = request.get_json()
    
    if ( "email" not in json_request.keys() ) :
        raise MissingRequiredField()

    usuario = ObtenerSocio(db_session, json_request["email"], json_request["username"], headers=request.headers).execute()
    if usuario is None :
        result = CrearSocio(session=db_session, headers=request.headers, json_request=json_request).execute()  
        return jsonify({'description':result}),200  
    else :
        return jsonify({'description' :"Usuario ya esta registrado"}),400
    
@administracion_blueprint.route('/socios', methods = ['GET'])
def obtener_socios():  
    return ObtenerSocios(session=db_session, headers=request.headers).execute()


@administracion_blueprint.route('/socios/<string:id_socio>', methods = ['GET'])
def get_socio_por_id(id_socio):
    return ObtenerSocioId(db_session, id=id_socio, headers=request.headers).execute()  
        
@administracion_blueprint.route('/socio/<string:id_socio>', methods = ['POST'])
def actualizar_socio(id_socio):
    json_request = request.get_json()
    
    if ( "email" not in json_request.keys() ) :
        raise MissingRequiredField()
    
    result = ActualizarSocio(session=db_session, id=id_socio, headers=request.headers, json_request=json_request).execute()  
    return jsonify({'description':result}),200  
    

#####################################################################
#                           Servicios                               #
#####################################################################

@administracion_blueprint.route('/producto_servicio', methods = ['POST'])
def crear_producto_servicio():  
    return CrearProductoServicio(session=db_session,  headers=request.headers,json_request=request.get_json()).execute()

@administracion_blueprint.route('/producto_servicio', methods = ['GET'])
def obtener_producto_servicio():  
    return ObtenerProductoServicios(session=db_session, headers=request.headers).execute()

#####################################################################
#                         Paises/Ciudades                           #
#####################################################################

@administracion_blueprint.route("/paises", methods = ['GET'])
def obtener_paises():
    return ObtenerPaises(session=db_session).execute()

@administracion_blueprint.route("/paises/<string:id_pais>/ciudades", methods = ['GET'])
def obtener_ciudades(id_pais):
    return ObtenerCiudades(session=db_session, id_pais=id_pais).execute()

#####################################################################
#                             Deportes                              #
#####################################################################

@administracion_blueprint.route("/deportes", methods = ['GET'])
def obtener_deportes():
    return ObtenerDeportes(session=db_session).execute()

#####################################################################
#                             Entrenadores                          #
#####################################################################

@administracion_blueprint.route('/entrenador', methods = ['POST'])
def crear_entrenador():
    json_request = request.get_json()
    
    if ( "email" not in json_request.keys() ) :
        raise MissingRequiredField()

    usuario = ObtenerEntrenador(db_session, json_request["email"], json_request["username"], headers=request.headers).execute()
    if usuario is None :
        result = CrearEntrenador(session=db_session, headers=request.headers, json_request=json_request).execute()  
        return jsonify({'description':result}),200  
    else :
        return jsonify({'description' :"Usuario ya esta registrado"}),400
    
@administracion_blueprint.route('/entrenadores', methods = ['GET'])
def obtener_entrenadores():  
    return ObtenerEntrenadores(session=db_session, headers=request.headers).execute()

#####################################################################
#                             Reuniones                             #
#####################################################################

@administracion_blueprint.route('/reunion', methods = ['POST'])
def crear_reunion():
    json_request = request.get_json()

    entrenador = ObtenerentrenadorId(db_session, json_request["id_entrenador"], headers=request.headers).execute()
    
    if len(entrenador[0]['respuesta'])==0:
        return jsonify({'description' :"No existe el entrenador especificado"}),400
    else :     
        result = CrearReunion(session=db_session, headers=request.headers, json_request=json_request).execute()  
        return jsonify({'description':result}),200  

@administracion_blueprint.route('/reuniones', methods = ['GET'])
def obtener_reuniones():  
    return ObtenerReuniones(session=db_session, headers=request.headers).execute()

@administracion_blueprint.route('/reuniones/disponibles', methods = ['GET'])
def obtener_reuniones_disponibles():  
    return ObteneReunionesDisponibles(session=db_session, headers=request.headers).execute()

@administracion_blueprint.route('/reunion/<string:id>/<string:id_usuario>', methods = ['POST'])
def asignar_reunion_usuario(id, id_usuario):    
    result = AsignarReunionUsuario(session=db_session, id=id, id_usuario=id_usuario, headers=request.headers).execute()  
    return jsonify({'description':result}),200  
