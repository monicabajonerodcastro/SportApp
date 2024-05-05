import uuid
from src.modelos.ubicacion import Ubicacion
from src.modelos.evento import Evento
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField
from src.servicios import auth
import re

class CrearEvento(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.headers = headers
        
        if "nombre" not in json_request.keys() or json_request["nombre"] == "":
            raise MissingRequiredField(parameter="Evento (nombre)")
        if "fecha_inicio" not in json_request.keys() or json_request["fecha_inicio"] == "":
            raise MissingRequiredField(parameter="Evento (fecha_inicio)")
        if "fecha_fin" not in json_request.keys() or json_request["fecha_fin"] == "":
            raise MissingRequiredField(parameter="Evento (fecha_fin)")
        if "id_deporte" not in json_request.keys() or json_request["id_deporte"] == "":
            raise MissingRequiredField(parameter="Evento (id_deporte)")
        if "id_socio" not in json_request.keys() or json_request["id_socio"] == "":
            raise MissingRequiredField(parameter="Evento (id_socio)")
        if "detalle" not in json_request.keys() or json_request["detalle"] == "":
            raise MissingRequiredField(parameter="Evento (detalle)")
        if "ubicacion" not in json_request.keys() or json_request["ubicacion"] == "":
            raise MissingRequiredField(parameter="Evento (ubicacion)")

        self.session = session
        nombre = json_request["nombre"]
        fecha_inicio = json_request["fecha_inicio"]
        fecha_fin = json_request["fecha_fin"]
        id_deporte = json_request["id_deporte"]
        id_socio = json_request["id_socio"]
        detalle = json_request["detalle"]
        ubicacion = json_request["ubicacion"]

        id=uuid.uuid4()
    
        self.evento = Evento(id=id, nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, id_deporte=id_deporte, id_socio=id_socio, detalle=detalle)
        self.ubicacion = Ubicacion(id_ubicacion=ubicacion["id"], direccion=ubicacion["direccion"], ubicacion_latitud=ubicacion["ubicacionLatitud"], 
                                   ubicacion_longitud=ubicacion["ubicacionLongitud"], nombre=ubicacion["nombre"], id_evento=id)
        
    def execute(self):
        
        auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.evento)
        self.session.add(self.ubicacion)
        self.session.commit()
        self.session.close()
        return "Evento registrado con éxito"
         
