
from sqlalchemy import JSON
from src.comandos.base_command import BaseCommand
from src.modelos.evento_usuario_u import EventoUsuarioU, EventoUsuarioUSchema
from src.servicios import auth


entrenmiento_schema = EventoUsuarioUSchema()

class ObtenerUsuariosEvento(BaseCommand):
    def __init__(self, session, id_evento, headers):
        self.session = session
        self.headers = headers
        self.id_plan = id_evento
        
        self.evento_usuarios_u = session.query(EventoUsuarioU).filter(EventoUsuarioU.id_evento == id_evento).all() 
 
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        respuesta = [entrenmiento_schema.dump(evento_usuarios_u) for evento_usuarios_u in self.evento_usuarios_u]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200
    