import jwt, os, datetime
from src.errors.errors import InvalidAuthentication
from src.services.secret import get_secret

secret_encode = get_secret(os.environ["PROJECT_ID"], "secret_jwt")

def generar_token(usuario):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=15),
        'iat': datetime.datetime.utcnow(),
        'sub': usuario
    }
    return jwt.encode(payload,secret_encode,algorithm='HS256')


def validar_token(token):
    try:  
        jwt.decode(jwt=token, key=secret_encode, algorithms=["HS256"])
        return "", 200
    except jwt.DecodeError:
        raise InvalidAuthentication(description="Error al decodificar el token")
    except jwt.ExpiredSignatureError:
        raise InvalidAuthentication(description="Token expirado")