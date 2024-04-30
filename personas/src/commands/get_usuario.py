from src.commands.base_command import BaseCommannd
from src.models.usuario import Usuario


class GetUsuario(BaseCommannd):
    def __init__(self, session, email):

        self.session = session
        self.user = self.session.query(Usuario).filter(Usuario.email == email).first()
    
    def execute(self):
        self.session.close()
        return self.user   

    