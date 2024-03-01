from flask import Blueprint, jsonify, request
from src.commands.crear_usuario import CrearUsuario
from src.commands.get_usuario import GetUsuario
from src.models.database import db_session

usuarios_blueprint = Blueprint('usuarios', __name__)

@usuarios_blueprint.route('/usuarios', methods = ['POST'])
def crear_usuario():
    json_request = request.get_json()
    result = CrearUsuario(db_session, json_request,request.headers).execute()  
    return jsonify({'msg':result}),201  
 
@usuarios_blueprint.route('/usuarios/<string:email>', methods=['GET'])
def obtener_usuario(email):
    result = GetUsuario(db_session, request.headers, email).execute()
    if result is not None :
        return jsonify({'nombre' : result.nombre, 'apellido': result.apellido, "email": result.email, "deportes_practica": result.deportes_practica}),200
    else :
        return jsonify({'msg' :"Usuario no existe"}),200