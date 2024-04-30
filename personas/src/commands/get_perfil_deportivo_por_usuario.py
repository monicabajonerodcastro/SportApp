from src.models.perfil_deportivo import PerfilDeportivo, PerfilDeportivoJsonSchema
from src.commands.base_command import BaseCommannd
from src.services.auth import validar_autenticacion
from src.errors.errors import NotFoundError, InvalidFormatField

from uuid import UUID

perfil_deportivo_schema = PerfilDeportivoJsonSchema()

class GetPerfilDeportivoPorUsuario(BaseCommannd):
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
        
        perfil_deportivo = self.session.query(PerfilDeportivo).filter(PerfilDeportivo.id_usuario == self.id_usuario).first()
        if perfil_deportivo is None:
            self.session.close()
            raise NotFoundError(description="El perfil deportivo no se encuentra registrado")
        self.session.close()
        return perfil_deportivo_schema.dump(perfil_deportivo), 200

    