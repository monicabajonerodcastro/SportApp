import jwt, os, datetime
from src.errors.errors import InvalidAuthentication
from src.services.secret import get_secret

if os.environ["ENVIRONMENT"] == 'prod':
    secret_encode = get_secret(os.environ["PROJECT_ID"], "secret_jwt")
else:
    secret_encode = "HPgBKB0wzo2NWbT"


def generar_token(usuario):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
        'iat': datetime.datetime.utcnow(),
        'sub': usuario
    }
    return jwt.encode(payload,secret_encode,algorithm='HS256')


def validar_token(token):
    try:  
        informacion = jwt.decode(jwt=token, key=secret_encode, algorithms=["HS256"])
        nuevo_token = generar_token(informacion["sub"])
        return {"token": nuevo_token, "id_usuario": informacion["sub"]}, 200
    except jwt.DecodeError:
        raise InvalidAuthentication(description="Error al decodificar el token")
    except jwt.ExpiredSignatureError:
        raise InvalidAuthentication(description="Token expirado")