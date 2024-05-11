from src.errores.errores import NotFoundError
from src.modelos.evento_deportista import EventoDeportista
from src.comandos.base_command import BaseCommand
from src.servicios import auth
from sqlalchemy import and_

class EliminarEventoDeportista(BaseCommand):
    def __init__(self, session, headers, id_evento) -> None:
        self.session = session
        self.headers = headers
        self.id_evento = id_evento

    def execute(self):
        usuario_id = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(headers=self.headers)
        evento_deportista = self.session.query(EventoDeportista).filter(and_(EventoDeportista.id_evento == self.id_evento, EventoDeportista.id_deportista == usuario_id)).first()
        if evento_deportista is not None:
            self.session.delete(evento_deportista)
            self.session.commit()
            self.session.close()
            return {"respuesta": "Evento eliminado correctamente de la agenda del deportista", "token" : token}, 200

        self.session.close()
        raise NotFoundError(description=f"El deportista no tiene asociado el evento [{self.id_evento}] o el evento no existe")