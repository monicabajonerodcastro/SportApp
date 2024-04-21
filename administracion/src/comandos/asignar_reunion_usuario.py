from src.modelos.reunion import Reunion
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField,InvalidFormatField
from src.servicios import auth
import re


class AsignarReunionUsuario(BaseCommand):
    def __init__(self, session, id, headers) -> None:
        self.id=id
        self.headers = headers
        self.session = session
        
   
    def execute(self):
        usuario = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True) 
        self.reunion = self.session.query(Reunion).filter(Reunion.id == self.id).one()
        self.reunion.id_usuario = usuario
        self.session.commit()
        self.session.close()
        return "Reunión asignada con éxito"