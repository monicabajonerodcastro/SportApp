from src.comandos.base_command import BaseCommand
from src.modelos.entrenador import Entrenador, EntrenadorJsonSchema
from src.servicios import auth

entrenador_schema=EntrenadorJsonSchema()

class ObtenerEntrenador(BaseCommand):
    def __init__(self, session, email, username, headers):

        self.session = session
        self.headers = headers
        self.entrenador = self.session.query(Entrenador).filter(Entrenador.email == email).first()
        if self.entrenador is None :
            self.entrenador = self.session.query(Entrenador).filter(Entrenador.username == username).first()
    
    def execute(self):
        auth.validar_autenticacion(headers=self.headers)
        self.session.close()
        return self.entrenador   
    
class ObtenerentrenadorId(BaseCommand):
    def __init__(self, session, id, headers):

        self.session = session
        self.headers = headers
        self.entrenador = self.session.query(Entrenador).filter(Entrenador.id == id).first()

    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        self.session.close()
        return {"respuesta" : entrenador_schema.dump(self.entrenador), "token" : nuevo_token},200
