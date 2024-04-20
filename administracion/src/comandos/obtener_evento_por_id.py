from src.modelos.evento import Evento, EventoJsonSchema
from src.comandos.base_command import BaseCommand
from src.servicios import auth, util
from src.errores.errores import NotFoundError, BadRequestError


evento_schema = EventoJsonSchema()

class ObtenerEventoId(BaseCommand):
    def __init__(self, session, headers, id_evento) -> None:
        self.session = session
        self.headers = headers
        self.id_evento = id_evento
       
    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        
        if util.is_valid_id(self.id_evento):
            evento = self.session.query(Evento).filter(Evento.id == self.id_evento).first()
            if evento is None:
                self.session.close()
                raise NotFoundError(description=f"No se encontró un evento con el id [{self.id_evento}]")

            respuesta = evento_schema.dump(evento)
            self.session.close()
            return {"respuesta": respuesta, "token" : token}, 200
        else:
            self.session.close()
            raise BadRequestError(description="El identificador del evento no es válido")
    