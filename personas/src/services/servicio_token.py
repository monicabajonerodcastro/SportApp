import jwt, os, datetime
from src.errors.errors import InvalidAuthentication

SECRET = os.environ["SECRET_JWT"]

def generar_token(usuario):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=15),
        'iat': datetime.datetime.utcnow(),
        'sub': usuario
    }
    return jwt.encode(payload,SECRET,algorithm='HS256')


def validar_token(token):
    try:  
        jwt.decode(jwt=token, key=SECRET, algorithms=["HS256"])
        return "", 200
    except jwt.DecodeError:
        raise InvalidAuthentication(description="Error al decodificar el token")
    except jwt.ExpiredSignatureError:
        raise InvalidAuthentication(description="Token expirado")