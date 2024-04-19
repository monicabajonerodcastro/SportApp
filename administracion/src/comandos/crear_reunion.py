from src.modelos.reunion import Reunion
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField,InvalidFormatField
from src.servicios import auth
import re

class CrearReunion(BaseCommand):
    def __init__(self, session, headers, json_request, test ) -> None:
        self.test=test
        self.headers = headers

        if ( "fecha" not in json_request.keys() or json_request["fecha"] =="" or
                "lugar" not in json_request.keys()  or   json_request["lugar"] =="" or
                    "id_entrenador" not in json_request.keys() or json_request["id_entrenador"] ==""):  
            raise MissingRequiredField()


        self.session = session
        fecha = json_request["fecha"]
        lugar = json_request["lugar"]
        entrenador = json_request["id_entrenador"]
    
        self.reunion = Reunion(fecha=fecha, lugar=lugar, entrenador=entrenador, usuario=None)
        
    def execute(self):
        if self.test==False:
            auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.reunion)
        self.session.commit()
        return "Reunión registrada con éxito"
         
