from src.commands.base_command import BaseCommannd
from src.models.usuario import Usuario, UsuarioJsonSchema
from src.errors.errors import MissingRequiredField,InvalidFormatField
from src.services import servicio_token
from sqlalchemy import and_
import re

usuario_schema = UsuarioJsonSchema()

class IngresarUsuario(BaseCommannd):
    def __init__(self, session, json_request):
        
        if ( "email" not in json_request.keys() or json_request["email"] == "" or
            "password" not in json_request.keys() or json_request["password"] == ""):
            raise MissingRequiredField(description="No se encontraron los parámetros para ingresar")

        self.session = session
        self.email = json_request["email"]
        self.password = json_request["password"]

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if not re.fullmatch(regex, self.email):
            raise InvalidFormatField
        
    def execute(self):
        user: Usuario
        user = self.session.query(Usuario).filter(and_(Usuario.email == self.email, Usuario.password == self.password)).first()
        if user is None:
            self.session.close()
            return {"description": "Usuario y/o contraseña inválidos"}, 400
        user_response = {}
        user_response["token"] = servicio_token.generar_token(usuario=str(user.id))
        user_response["rol"] = user.rol
        self.session.close()
        return user_response, 200 

    