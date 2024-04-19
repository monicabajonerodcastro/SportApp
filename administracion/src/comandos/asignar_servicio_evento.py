from src.modelos.evento_servicio import EventoServicio
from src.comandos.base_command import BaseCommand
from src.errores.errores import BadRequestError
from src.servicios import auth
from sqlalchemy import and_

class AsignarServicioEvento(BaseCommand):
    def __init__(self, session, headers, evento, servicio) -> None:
        self.session = session
        self.headers = headers
        self.evento = evento
        self.servicio = servicio
       
    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        
        evento_servicio = self.session.query(EventoServicio).filter(and_(EventoServicio.id_evento == self.evento["id"], EventoServicio.id_servicio == self.servicio["id"])).first()
        if evento_servicio is None:
            nuevo_evento_servicio = EventoServicio(self.evento["id"], self.servicio["id"])
            self.session.add(nuevo_evento_servicio)
            self.session.commit()
            return {"respuesta": "Servicio asignado correctamente al evento", "token" : token}, 200

        evento_nombre = self.evento["nombre"]
        servicio_nombre = self.servicio["nombre"]
        raise BadRequestError(description=f"El evento [{evento_nombre}] ya tiene el servicio [{servicio_nombre}] asociado")

        
    