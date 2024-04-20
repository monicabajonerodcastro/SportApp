from src.errores.errores import NotFoundError
from src.comandos.base_command import BaseCommand
from src.servicios import auth, http
import os

HOST_PERSONAS = os.environ["HOST_PERSONAS"]

class ObtenerDeportistaId(BaseCommand):
    def __init__(self, headers, id_deportista) -> None:
        self.headers = headers
        self.id_deportista = id_deportista

    def execute(self):
        id_usuario = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True) 
        usuario_respuesta = http.get_request(url=f"{HOST_PERSONAS}/personas/{id_usuario}", headers=self.headers)
        
        usuario_respuesta_status_code = usuario_respuesta.status_code
        if usuario_respuesta_status_code < 200 or usuario_respuesta_status_code > 209:
            raise NotFoundError(description="No se encontró el deportista seleccionado, por favor verifique la información")
        return usuario_respuesta.json(), usuario_respuesta_status_code