from src.comandos.base_command import BaseCommand
from src.modelos.socio import Socio


class ObtenerSocio(BaseCommand):
    def __init__(self, session, email, username):

        self.session = session
        self.socio = self.session.query(Socio).filter(Socio.email == email).first()
        if self.socio is None :
            self.socio = self.session.query(Socio).filter(Socio.username == username).first()
    
    def execute(self):
        return self.socio   
