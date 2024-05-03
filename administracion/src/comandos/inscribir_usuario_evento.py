from src.modelos.evento import Evento
from src.modelos.evento_usuario_u import EventoUsuarioU
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField, NotFoundError
from src.servicios import auth
import re

class InscribirUsuarioEvento(BaseCommand):
    def __init__(self, session, headers, id_evento) -> None:
        self.headers = headers

        if id_evento == "":
            raise MissingRequiredField(parameter="EventoU (id_evento)")

        self.session = session
        self.id_evento = id_evento

        evento = self.session.query(Evento).filter(Evento.id == self.id_evento).first()
        if evento is None:
            raise NotFoundError(description="No existe evento con id "+ id_evento)        
        
    def execute(self):
        usuario = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True) 
        self.evento_u = EventoUsuarioU(id_usuario=usuario, id_evento=self.id_evento)
        self.session.add(self.evento_u)
        self.session.commit()
        self.session.close()
        return "Inscripción registrada con éxito"