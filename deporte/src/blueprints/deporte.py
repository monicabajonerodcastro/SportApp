from flask import Blueprint, jsonify

deporte_blueprint = Blueprint('deporte', __name__, url_prefix="/deporte")

#####################################################################
#                          Health Check                             #
#####################################################################

@deporte_blueprint.route('/health-check', methods = ['GET'])
def health_check():
    return jsonify({"description":"UP"}),200  
