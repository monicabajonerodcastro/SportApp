from flask import Blueprint, jsonify, request
from src.commands.crear_usuario import CrearUsuario
from src.commands.get_usuario import GetUsuario
from src.commands.crear_perfil_deportivo import CrearPerfilDeportivo
from src.models.database import db_session
from src.errors.errors import MissingRequiredField

personas_blueprint = Blueprint('personas', __name__,url_prefix="/personas")


@personas_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({"mensaje":"UP"}),200     

@personas_blueprint.route('/usuario', methods = ['POST'])
def crear_usuario():
    json_request = request.get_json()
    
    if ( "email" not in json_request.keys() ) :
        raise MissingRequiredField()

    usuario = GetUsuario(db_session, request.headers,  json_request["email"]).execute()
    if usuario is None :
            result = CrearUsuario(db_session, json_request,request.headers).execute()  
            return jsonify({'msg':result}),201  
    else :
        return jsonify({'msg' :"Usuario ya esta registrado"}),200

 
@personas_blueprint.route('/usuario/<string:email>', methods=['GET'])
def obtener_usuario(email):
    result = GetUsuario(db_session, request.headers, email).execute()
    if result is not None :
        return jsonify({'id' : result.id,'nombre' : result.nombre, 'apellido': result.apellido, "email": result.email}),200
    else :
        return jsonify({'msg' :"Usuario no existe"}),200
    

 
@personas_blueprint.route('/perildeportivo', methods = ['POST'])
def crear_perfil_deportivo():
    json_request = request.get_json()
    
    result = CrearPerfilDeportivo(db_session, json_request).execute()  
    return jsonify({'msg':result}),201  
    