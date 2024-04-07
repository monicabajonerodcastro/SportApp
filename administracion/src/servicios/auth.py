from src.errores.errores import InvalidAuthenticationError
from src.servicios import http
import os

HOST_PERSONAS = os.environ["HOST_PERSONAS"]

def validar_autenticacion(headers):
    if 'Authorization' not in headers:
        raise InvalidAuthenticationError(code=403, description="No se encontró el header de autorización")

    authorization_header = headers["Authorization"]
    if "Bearer" not in authorization_header:
        raise InvalidAuthenticationError(code=403, description="El header de autorización no tiene un formato correcto")
    
    token = authorization_header.split("Bearer")[1].strip()
    body = {
        "token": token
    }
    validacion_token = http.post_request(url=f"{HOST_PERSONAS}/personas/validar-token", data=body)
    estado_auth = validacion_token.status_code
    if estado_auth == 401:
        raise InvalidAuthenticationError(code=estado_auth, description=validacion_token.json()["description"])
    if estado_auth == 400:
        raise InvalidAuthenticationError(code=estado_auth, description="El token de autenticación no tiene un formato correcto")
    if estado_auth < 200 or estado_auth > 209:
        raise InvalidAuthenticationError(code=estado_auth, description=validacion_token.text)

