
from src.comandos.base_command import BaseCommand
from src.modelos.evento import Evento, EventoJsonSchema
from src.servicios import auth

evento_schema = EventoJsonSchema()

class ObtenerEventos(BaseCommand):
    def __init__(self, session, headers):
        self.session = session
        self.headers = headers
    
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        eventos = self.session.query(Evento).all() 
        respuesta = [evento_schema.dump(evento) for evento in eventos]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200