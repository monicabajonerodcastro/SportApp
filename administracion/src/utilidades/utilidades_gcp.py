
import os

def obtener_secreto(project_id: str, secret_id: str) -> None:

    from google.cloud import secretmanager

    cliente = secretmanager.SecretManagerServiceClient()
    nombre = cliente.secret_path(project_id, secret_id)

    nombre_secreto = cliente.secret_version_path(project_id, secret_id, 1)

    respuesta = cliente.access_secret_version(name=nombre_secreto)

    payload = respuesta.payload.data.decode('UTF-8')
    print(payload)
    return payload

    #return payload projects/52394347692/secrets/postgres_password/versions/1