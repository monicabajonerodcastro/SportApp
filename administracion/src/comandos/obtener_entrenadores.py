
from src.comandos.base_command import BaseCommand
from src.modelos.entrenador import Entrenador, EntrenadorJsonSchema
from src.servicios import auth

entrenador_schema = EntrenadorJsonSchema()

class ObtenerEntrenadores(BaseCommand):
    def __init__(self, session, headers, test):
        self.session = session
        self.headers = headers
        
    
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)

        self.entrenadores = self.session.query(Entrenador).all() 
        respuesta = [entrenador_schema.dump(entrenador) for entrenador in self.entrenadores]
        return {"respuesta": respuesta, "token": nuevo_token}, 200