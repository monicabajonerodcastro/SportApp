from src.errores.errores import BadRequestError
from src.modelos.servicio_deportista import ServicioDeportista
from src.comandos.base_command import BaseCommand
from src.servicios import auth
from sqlalchemy import and_

class AsignarServicioDeportista(BaseCommand):
    def __init__(self, session, headers, servicio, deportista) -> None:
        self.session = session
        self.headers = headers
        self.servicio = servicio
        self.deportista = deportista

    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        
        servicio_deportista = self.session.query(ServicioDeportista).filter(and_(ServicioDeportista.id_servicio == self.servicio["id"], ServicioDeportista.id_deportista == self.deportista["id"])).first()
        if servicio_deportista is None:
            nuevo_evento_servicio = ServicioDeportista(self.servicio["id"], self.deportista["id"])
            self.session.add(nuevo_evento_servicio)
            self.session.commit()
            self.session.close()
            return {"respuesta": "Servicio asignado correctamente al deportista", "token" : token}, 200

        deportista_nombre = self.deportista["nombre"]
        servicio_nombre = self.servicio["nombre"]
        self.session.close()
        raise BadRequestError(description=f"El deportista [{deportista_nombre}] ya tiene asociado el servicio [{servicio_nombre}] asociado")