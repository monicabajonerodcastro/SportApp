from src.modelos.evento import Evento
from src.comandos.base_command import BaseCommand
from src.errores.errores import BadRequestError, MissingRequiredField
from src.servicios import auth
import re

class ActualizarEvento(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.headers = headers
        
        if "id" not in json_request.keys() or json_request["id"] == "":
            raise MissingRequiredField(parameter="Evento (id)")
        if "fecha_inicio" not in json_request.keys() or json_request["fecha_inicio"] == "":
            raise MissingRequiredField(parameter="Evento (fecha_inicio)")
        if "fecha_fin" not in json_request.keys() or json_request["fecha_fin"] == "":
            raise MissingRequiredField(parameter="Evento (fecha_fin)")


        self.session = session
        id = json_request["id"]
        fecha_inicio = json_request["fecha_inicio"]
        fecha_fin = json_request["fecha_fin"]

        self.evento = self.session.query(Evento).filter(Evento.id==id).one()
        if self.evento  is not None:
            self.evento.fecha_inicio =  fecha_inicio
            self.evento.fecha_fin =  fecha_fin
        else :
            raise BadRequestError(description=f"El evento [{id}] no existe")

       
    def execute(self):
        
        #auth.validar_autenticacion(headers=self.headers)
        self.session.commit()
        self.session.close()
        return "Evento actualizado con exito"
         
