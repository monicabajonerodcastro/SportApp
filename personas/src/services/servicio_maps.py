import os
from src.services.secret import get_secret

def obtener_maps_key():
    if os.environ["ENVIRONMENT"] == 'prod':
        return "AIzaSyD-Ee0CfpR_bDyabJ9zJyNtSBa3Ndt4W2M"
    else:
        return "MAPS_KEY"

