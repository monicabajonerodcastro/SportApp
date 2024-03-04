
from src.commands.base_command import BaseCommannd
from src.services.publicar_mensaje import publicar_mensaje
import json



class EnviarAlerta(BaseCommannd):
    def __init__(self, json_request):
        self.tipo_alerta: str = "NUTRICION"
        self.mensaje: str = json_request["mensaje"]

    def execute(self):
        mensaje_dict = {
            "tipo": self.tipo_alerta,
            "mensaje": self.mensaje
        }
        publicar_mensaje(mensaje=json.dumps(mensaje_dict))
