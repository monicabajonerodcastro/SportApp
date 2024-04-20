from src.comandos.base_command import BaseCommand
from src.modelos.producto_servicio import ProductoServicio, ProductoServicioSchema
from src.servicios import auth, util
from src.errores.errores import NotFoundError, BadRequestError
servicio_schema = ProductoServicioSchema()


class ObtenerProductoServicioId(BaseCommand):
    def __init__(self, session, headers, id_servicio) -> None:
        self.session = session
        self.headers = headers
        self.id_servicio = id_servicio
       
    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)

        if util.is_valid_id(self.id_servicio):
            servicio = self.session.query(ProductoServicio).filter(ProductoServicio.id == self.id_servicio).first()
            if servicio is None:
                self.session.close()
                raise NotFoundError(description=f"No se encontró un producto y/o servicio con el id [{self.id_servicio}]")

            respuesta = servicio_schema.dump(servicio)
            self.session.close()
            return {"respuesta": respuesta, "token" : token}, 200
        else:
            self.session.close()
            raise BadRequestError(description="El identificador del servicio no es válido")
    