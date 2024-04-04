from flask import Blueprint, jsonify, request
from src.commands.crear_usuario import CrearUsuario
from src.commands.ingresar_usuario import IngresarUsuario
from src.commands.get_usuario import GetUsuario
from src.commands.crear_perfil_deportivo import CrearPerfilDeportivo
from src.commands.validar_token import ValidarToken
from src.models.database import db_session
from src.errors.errors import MissingRequiredField

personas_blueprint = Blueprint('personas', __name__,url_prefix="/personas")


@personas_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({"description":"UP"}),200     

@personas_blueprint.route('/usuario', methods = ['POST'])
def crear_usuario():
    json_request = request.get_json()
    
    if ( "email" not in json_request.keys() ) :
        raise MissingRequiredField()

    usuario = GetUsuario(db_session, json_request["email"]).execute()
    if usuario is None :
        result = CrearUsuario(db_session, json_request).execute()  
        return jsonify({'description':result}),201  
    else :
        return jsonify({'description' :"Usuario ya esta registrado"}),400

 
@personas_blueprint.route('/perfildeportivo', methods = ['POST'])
def crear_perfil_deportivo():
    json_request = request.get_json()
    
    result = CrearPerfilDeportivo(db_session, json_request).execute()  
    return jsonify({'description':result}),201  


@personas_blueprint.route('/ingresar', methods=["POST"])
def ingresar_usuario():
    json_request = request.get_json()
    return IngresarUsuario(session=db_session, json_request=json_request).execute()

@personas_blueprint.route('/validar-token', methods=["POST"])
def validar_token():
    json_request = request.get_json()
    return ValidarToken(json_request=json_request).execute()

     

