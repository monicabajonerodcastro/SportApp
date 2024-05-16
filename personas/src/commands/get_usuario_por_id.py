from src.models.direccion import Direccion, DireccionSchema
from src.commands.base_command import BaseCommannd
from src.models.usuario import Usuario, UsuarioJsonSchema
from src.services.auth import validar_autenticacion
from src.errors.errors import NotFoundError, InvalidFormatField

from uuid import UUID

usuario_schema = UsuarioJsonSchema()
direccion_schema = DireccionSchema()

class GetDireccionPorId(BaseCommannd):
    def __init__(self, session, headers, id_usuario) -> None:
        self.session = session
        self.headers = headers
        self.id_usuario = id_usuario

    def execute(self):
        validar_autenticacion(self.headers)
        direccion = self.session.query(Direccion).filter(Direccion.id_usuario == self.id_usuario).first()
        direccion_response = direccion_schema.dump(direccion)
        self.session.close()
        return direccion_response, 200

class GetUsuarioPorId(BaseCommannd):
    def __init__(self, session, headers, id_usuario):

        self.session = session
        self.headers = headers
        self.id_usuario = id_usuario

    def _is_valid_id(self, uuid: str, version: int = 4) -> bool:
        try:
            uuid_obj = UUID(uuid, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid
    
    def execute(self):
        validar_autenticacion(self.headers)

        if not self._is_valid_id(self.id_usuario):
            raise InvalidFormatField(description=f"El usuario [{self.id_usuario}] no tiene un formato uuid correcto")
        
        user = self.session.query(Usuario).filter(Usuario.id == self.id_usuario).first()
        if user is None:
            self.session.close()
            raise NotFoundError(description="El usuario no se encuentra registrado")
        direccion = self.session.query(Direccion).filter(Direccion.id_usuario == user.id).first()
        usuario_response = usuario_schema.dump(user)
        direccion_response = direccion_schema.dump(direccion)
        usuario_response["direccion"] = direccion_response
        self.session.close()
        return usuario_response, 200

    