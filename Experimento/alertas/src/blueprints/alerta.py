from flask import Blueprint, jsonify, request
from src.commands.enviar_alerta import EnviarAlerta

alertas_blueprint = Blueprint('alertas', "/alertas")

@alertas_blueprint.route('/status', methods = ['get'])
def health_check():
    return jsonify({'msg':"UP"}),200 

@alertas_blueprint.route('/enviar-alerta', methods = ['POST'])
def enviar_alerta():
    json_request = request.get_json()
    result = EnviarAlerta(json_request).execute()
    return jsonify({'msg':result}),200 
 
