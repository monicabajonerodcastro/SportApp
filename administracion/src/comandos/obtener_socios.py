
from src.comandos.base_command import BaseCommand
from src.modelos.socio import Socio, SocioJsonSchema
from src.servicios import auth

socio_schema = SocioJsonSchema()

class ObtenerSocios(BaseCommand):
    def __init__(self, session, headers, test):
        self.session = session
        self.headers = headers
        self.test = test
        
    
    def execute(self):
        if self.test==False:
            auth.validar_autenticacion(headers=self.headers)
        self.socios = self.session.query(Socio).all() 
        return [socio_schema.dump(plan) for plan in self.socios], 200  


