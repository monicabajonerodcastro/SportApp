from src.modelos.reunion import Reunion
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField,InvalidFormatField
from src.servicios import auth
import re


class AsignarReunionUsuario(BaseCommand):
    def __init__(self, session, id, id_usuario, headers) -> None:
        self.id=id
        self.id_usuario=id_usuario
        self.headers = headers

        self.session = session
        self.reunion = self.session.query(Reunion).filter(Reunion.id == self.id).one()
        self.reunion.id_usuario = self.id_usuario
   
    def execute(self):
        auth.validar_autenticacion(headers=self.headers)
        
        self.session.commit()
        return "Reunión asignada con éxito"