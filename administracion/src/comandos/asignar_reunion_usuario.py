from src.modelos.reunion import Reunion
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField,InvalidFormatField
from src.servicios import auth
import re
from src.servicios import auth


class AsignarReunionUsuario(BaseCommand):
    def __init__(self, session, id, headers) -> None:
        self.id=id
        self.headers = headers
        self.id_usuario=auth.validar_autenticacion(self.headers, retornar_usuario=True) 
        self.session = session
        self.reunion = self.session.query(Reunion).filter(Reunion.id == self.id).one()
        self.reunion.id_usuario = self.id_usuario
   
    def execute(self):
        auth.validar_autenticacion(headers=self.headers)
        
        self.session.commit()
        self.session.close()
        return "Reunión asignada con éxito"