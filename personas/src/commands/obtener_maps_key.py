
from src.services.auth import validar_autenticacion
from src.services.servicio_maps import obtener_maps_key
from src.commands.base_command import BaseCommannd


class ObtenerMapsKey(BaseCommannd):
    def __init__(self) -> None:
        pass

    def execute(self):
        return {"key" : obtener_maps_key()}, 200
