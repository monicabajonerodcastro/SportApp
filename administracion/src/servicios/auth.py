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
    if estado_auth < 200 or estado_auth > 209:
        mensaje_auth = validacion_token.json()
        raise InvalidAuthenticationError(code=estado_auth, description=mensaje_auth["msg"])
