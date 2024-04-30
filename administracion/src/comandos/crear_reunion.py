from src.modelos.reunion import Reunion
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField,InvalidFormatField
from src.servicios import auth
import re

class CrearReunion(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.headers = headers
        
        if "fecha" not in json_request.keys() or json_request["fecha"] == "":
            raise MissingRequiredField(parameter="Reunion (fecha)")
        if "lugar" not in json_request.keys() or json_request["lugar"] == "":
            raise MissingRequiredField(parameter="Reunion (lugar)")
        if "id_entrenador" not in json_request.keys() or json_request["id_entrenador"] == "":
            raise MissingRequiredField(parameter="Reunion (id_entrenador)")

        self.session = session
        fecha = json_request["fecha"]
        lugar = json_request["lugar"]
        entrenador = json_request["id_entrenador"]
    
        self.reunion = Reunion(fecha=fecha, lugar=lugar, entrenador=entrenador, usuario=None)
        
    def execute(self):
        auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.reunion)
        self.session.commit()
        self.session.close()
        return "Reunión registrada con éxito"
         
