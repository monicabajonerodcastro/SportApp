from flask import Blueprint, jsonify

alertas_blueprint = Blueprint('alertas', __name__, url_prefix="/alertas")

@alertas_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({'msg':"UP"}),200  
 
