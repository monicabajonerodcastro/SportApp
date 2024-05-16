from src.errors.errors import InvalidAuthentication
from src.services import servicio_token

def validar_autenticacion(headers):
    if 'Authorization' not in headers:
        raise InvalidAuthentication(code=403, description="No se encontró el header de autorización")

    authorization_header = headers["Authorization"]
    if "Bearer" not in authorization_header:
        raise InvalidAuthentication(code=403, description="El header de autorización no tiene un formato correcto")
    
    token = authorization_header.split("Bearer")[1].strip()
    (_, estado_auth) = servicio_token.validar_token(token=token)
    return estado_auth

def obtener_usuario_id(headers):
    authorization_header = headers["Authorization"]
    token = authorization_header.split("Bearer")[1].strip()
    (info_token, _) = servicio_token.validar_token(token=token)
    return info_token["id_usuario"]

