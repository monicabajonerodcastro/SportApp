
from src.modelos.producto_servicio import ProductoServicio, ProductoServicioSchema
from src.modelos.evento_servicio import EventoServicio
from src.comandos.base_command import BaseCommand
from src.servicios import auth

producto_servicio_schema = ProductoServicioSchema()

class ObtenerServiciosPorEvento(BaseCommand):
    def __init__(self, session, headers, evento) -> None:
        self.session = session
        self.headers = headers
        self.evento = evento
        self.servicios = []

    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        evento_servicios = self.session.query(EventoServicio).filter(EventoServicio.id_evento == self.evento["id"]).all()
        if len(evento_servicios) > 0:
            for servicio in evento_servicios:
                producto_servicio = self.session.query(ProductoServicio).filter(ProductoServicio.id == servicio.id_servicio).first()
                self.servicios.append(producto_servicio)
        respuesta = [producto_servicio_schema.dump(serv) for serv in self.servicios]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200
        