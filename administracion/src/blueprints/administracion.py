from flask import Blueprint, jsonify, request
from src.comandos.obtener_plan_por_id import ObtenerPlanId
from src.comandos.obtener_planes import ObtenerPlan
from src.modelos.database import db_session

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