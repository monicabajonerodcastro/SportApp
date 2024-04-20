
from sqlalchemy import JSON
from src.comandos.base_command import BaseCommand
from src.modelos.reunion import Reunion, ReunionJsonSchema
from src.servicios import auth

reunion_schema = ReunionJsonSchema()

class ObtenerReuniones(BaseCommand):
    def __init__(self, session, headers):
        self.session = session
        self.headers = headers
        
    
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)

        self.reuniones = self.session.query(Reunion).all()
        respuesta = [reunion_schema.dump(reunion) for reunion in self.reuniones]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200
    
class ObteneReunionesDisponibles(BaseCommand):
    def __init__(self, session, headers):

        self.session = session
        self.headers = headers
        self.reuniones = session.query(Reunion).filter(Reunion.id_usuario == None).all() 
  
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        respuesta = [reunion_schema.dump(reunion) for reunion in self.reuniones]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200
    
    