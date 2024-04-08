from flask import Blueprint, jsonify, request
from src.comandos.obtener_plan_por_id import ObtenerPlanId
from src.comandos.obtener_planes import ObtenerPlan
from src.comandos.asignar_deportista_a_plan import AsignarDeportistaPlan
from src.modelos.database import db_session

from flask import Blueprint, jsonify, request
from src.comandos.crear_socio import CrearSocio
from src.comandos.obtener_socio import ObtenerSocio
from src.comandos.obtener_socios import ObtenerSocios
from src.errores.errores import MissingRequiredField

administracion_blueprint = Blueprint('administracion', __name__, url_prefix="/administracion")

@administracion_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({"description":"UP"}),200  

@administracion_blueprint.route('/plan', methods = ['GET'])
def obtener_planes():
    return ObtenerPlan(session=db_session, headers=request.headers).execute()

@administracion_blueprint.route('/plan/<string:id_plan>', methods = ['GET'])
def get_plan_por_id(id_plan):
    return ObtenerPlanId(session=db_session, headers=request.headers, id_plan=id_plan).execute()

@administracion_blueprint.route('/plan/deportista', methods=["POST"])
def asignar_deportista_a_plan():
    return AsignarDeportistaPlan(session=db_session, headers=request.headers, json_request=request.get_json()).execute()

@administracion_blueprint.route('/socio', methods = ['POST'])
def crear_socio():
    json_request = request.get_json()
    
    if ( "email" not in json_request.keys() ) :
        raise MissingRequiredField()

    usuario = ObtenerSocio(db_session, json_request["email"], json_request["username"], headers=request.headers).execute()
    if usuario is None :
        result = CrearSocio(session=db_session, headers=request.headers, json_request=json_request, test=False).execute()  
        return jsonify({'description':result}),201  
    else :
        return jsonify({'description' :"Usuario ya esta registrado"}),400
    
@administracion_blueprint.route('/socios', methods = ['GET'])
def obtener_socios():  
    return ObtenerSocios(session=db_session, headers=request.headers,test=False).execute()
