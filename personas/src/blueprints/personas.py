from flask import Blueprint, jsonify, request
from src.commands.obtener_maps_key import ObtenerMapsKey
from src.commands.get_perfil_deportivo_por_usuario import GetPerfilDeportivoPorUsuario
from src.commands.crear_usuario import CrearUsuario
from src.commands.ingresar_usuario import IngresarUsuario
from src.commands.get_usuario import GetUsuario
from src.commands.crear_perfil_deportivo import CrearPerfilDeportivo
from src.commands.get_usuario_por_id import GetDireccionPorId, GetUsuarioPorId
from src.commands.validar_token import ValidarToken
from src.models.database import db_session
from src.errors.errors import MissingRequiredField

personas_blueprint = Blueprint('personas', __name__,url_prefix="/personas")

#####################################################################
#                          Health Check                             #
#####################################################################

@personas_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({"description":"UP"}),200     

#####################################################################
#                            Utilidades                             #
#####################################################################

@personas_blueprint.route('/maps', methods = ['GET'])
def obtener_key_maps():
    return ObtenerMapsKey().execute()

#####################################################################
#                             Usuarios                              #
#####################################################################

@personas_blueprint.route('/usuario', methods = ['POST'])
def crear_usuario():
    json_request = request.get_json()
    
    if ( "email" not in json_request.keys() ) :
        raise MissingRequiredField(description="No se encontró el email en la petición")

    usuario = GetUsuario(db_session, json_request["email"]).execute()
    if usuario is None :
        result = CrearUsuario(db_session, json_request).execute()  
        return result,201  
    else :
        return jsonify({'description' :"Usuario ya esta registrado"}),400

@personas_blueprint.route('/<string:id_persona>', methods=["GET"])
def obtener_usuario_por_id(id_persona):
    return GetUsuarioPorId(session=db_session, headers=request.headers, id_usuario=id_persona).execute()

@personas_blueprint.route('/direccion/<string:id_persona>', methods=["GET"])
def obtener_direccion_por_id(id_persona):
    return GetDireccionPorId(session=db_session, headers=request.headers, id_usuario=id_persona).execute()

#####################################################################
#                         Perfil Deportivo                          #
#####################################################################


@personas_blueprint.route('/perfildeportivo/<string:id_persona>', methods = ['GET'])
def obtener_perfil_deportivo_por_id_usuario(id_persona):
    return GetPerfilDeportivoPorUsuario(session=db_session, headers=request.headers, id_usuario=id_persona).execute()

@personas_blueprint.route('/perfildeportivo', methods = ['POST'])
def crear_perfil_deportivo():
    json_request = request.get_json()
    
    result = CrearPerfilDeportivo(db_session, json_request).execute()  
    return result,201  

#####################################################################
#                           Autenticación                           #
#####################################################################

@personas_blueprint.route('/ingresar', methods=["POST"])
def ingresar_usuario():
    json_request = request.get_json()
    return IngresarUsuario(session=db_session, json_request=json_request).execute()

@personas_blueprint.route('/validar-token', methods=["POST"])
def validar_token():
    json_request = request.get_json()
    return ValidarToken(json_request=json_request).execute()


     

