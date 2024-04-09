from src.comandos.base_command import BaseCommand
from src.modelos.socio import Socio
from src.servicios import auth


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
