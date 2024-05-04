from src.errores.errores import BadRequestError
from src.modelos.evento_deportista import EventoDeportista
from src.comandos.base_command import BaseCommand
from src.servicios import auth
from sqlalchemy import and_

class AsignarEventoDeportista(BaseCommand):
    def __init__(self, session, headers, evento) -> None:
        self.session = session
        self.headers = headers
        self.evento = evento

    def execute(self):
        usuario_id = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(headers=self.headers)
        evento_deportista = self.session.query(EventoDeportista).filter(and_(EventoDeportista.id_evento == self.evento["id"], EventoDeportista.id_deportista == usuario_id)).first()
        if evento_deportista is None:
            nuevo_evento_deportista = EventoDeportista(self.evento["id"], usuario_id)
            self.session.add(nuevo_evento_deportista)
            self.session.commit()
            self.session.close()
            return {"respuesta": "Evento asignado correctamente al deportista", "token" : token}, 200

        evento_nombre = self.evento["nombre"]
        self.session.close()
        raise BadRequestError(description=f"El deportista ya tiene asociado el evento [{evento_nombre}] asociado")