from src.comandos.base_command import BaseCommand
from src.modelos.socio import Socio, SocioJsonSchema
from src.servicios import auth

socio_schema=SocioJsonSchema()

class ObtenerSocio(BaseCommand):
    def __init__(self, session, email, username, headers):

        self.session = session
        self.headers = headers
        self.socio = self.session.query(Socio).filter(Socio.email == email).first()
        if self.socio is None :
            self.socio = self.session.query(Socio).filter(Socio.username == username).first()
    
    def execute(self):
        auth.validar_autenticacion(headers=self.headers)
        return self.socio   
    
class ObtenerSocioId(BaseCommand):
    def __init__(self, session, id, headers):

        self.session = session
        self.headers = headers
        self.socio = self.session.query(Socio).filter(Socio.id == id).first()

    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        return {"respuesta" : socio_schema.dump(self.socio), "token" : nuevo_token},200
