from src.errores.errores import BadRequestError
from src.modelos.servicio_deportista import ServicioDeportista
from src.comandos.base_command import BaseCommand
from src.servicios import auth
from sqlalchemy import and_

class AsignarServicioDeportista(BaseCommand):
    def __init__(self, session, headers, servicio) -> None:
        self.session = session
        self.headers = headers
        self.servicio = servicio

    def execute(self):
        usuario_id = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(headers=self.headers)
        
        servicio_deportista = self.session.query(ServicioDeportista).filter(and_(ServicioDeportista.id_servicio == self.servicio["id"], ServicioDeportista.id_deportista == usuario_id)).first()
        if servicio_deportista is None:
            nuevo_evento_servicio = ServicioDeportista(self.servicio["id"], usuario_id)
            self.session.add(nuevo_evento_servicio)
            self.session.commit()
            self.session.close()
            return {"respuesta": "Servicio asignado correctamente al deportista", "token" : token}, 200

        servicio_nombre = self.servicio["nombre"]
        self.session.close()
        raise BadRequestError(description=f"El deportista ya tiene asociado el servicio [{servicio_nombre}] asociado")