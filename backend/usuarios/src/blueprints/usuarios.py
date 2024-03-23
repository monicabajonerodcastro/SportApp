from flask import Blueprint, jsonify

usuarios_blueprint = Blueprint('usuarios', __name__, url_prefix="/usuarios")

@usuarios_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({'msg':"UP"}),200  
 
