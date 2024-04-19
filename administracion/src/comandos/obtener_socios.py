
from src.comandos.base_command import BaseCommand
from src.modelos.socio import Socio, SocioJsonSchema
from src.servicios import auth

socio_schema = SocioJsonSchema()

class ObtenerSocios(BaseCommand):
    def __init__(self, session, headers):
        self.session = session
        self.headers = headers
        
    
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)

        self.socios = self.session.query(Socio).all() 
        respuesta = [socio_schema.dump(socio) for socio in self.socios]
        return {"respuesta": respuesta, "token": nuevo_token}, 200
    


