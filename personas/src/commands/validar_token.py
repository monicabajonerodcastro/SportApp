from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredField
from src.services import servicio_token

class ValidarToken(BaseCommannd):
    def __init__(self, json_request):
        if ( "token" not in json_request.keys() or json_request["token"] == ""):
            raise MissingRequiredField()
        self.token = json_request["token"]
    
    def execute(self):
        return servicio_token.validar_token(token=self.token)