import os
from src.services.secret import get_secret

def obtener_maps_key():
    if os.environ["ENVIRONMENT"] == 'prod':
        return get_secret(os.environ["PROJECT_ID"], "maps_key")
    else:
        return "MAPS_KEY"

