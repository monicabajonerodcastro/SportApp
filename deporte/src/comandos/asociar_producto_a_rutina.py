from src.modelos.rutina_alimenticia import RutinaAlimenticia
from src.modelos.producto_rutina import ProductoRutina
from src.errores.errores import BadRequestError, MissingRequiredField, NotFoundError
from src.comandos.base_command import BaseCommand
from src.servicios import auth
from sqlalchemy import and_


class AsociarProductoARutina(BaseCommand):
    def __init__(self, session, headers, id_rutina_alimenticia, json_request) -> None:
        self.session = session
        self.headers = headers
        self.id_rutina_alimenticia = id_rutina_alimenticia

        if "dosis" not in json_request.keys() or json_request["dosis"] == "":
            raise MissingRequiredField(parameter="dosis")
        if "producto_id" not in json_request.keys() or json_request["producto_id"] == "":
            raise MissingRequiredField(parameter="producto_id")
        
        self.dosis = json_request["dosis"]
        self.producto_id = json_request["producto_id"]

        self.producto_rutina = ProductoRutina(self.producto_id, self.dosis, self.id_rutina_alimenticia)

    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        rutina_alimenticia = self.session.query(RutinaAlimenticia).filter(RutinaAlimenticia.id == self.id_rutina_alimenticia).first()
        if rutina_alimenticia is None:
            raise NotFoundError(description=f"No existe la rutina alimenticia con id [{self.id_rutina_alimenticia}]")

        producto_rutina_old = self.session.query(ProductoRutina).filter(and_(ProductoRutina.producto_id == self.producto_id, ProductoRutina.rutina_alimenticia == self.id_rutina_alimenticia)).first()
        if producto_rutina_old is None:
            self.session.add(self.producto_rutina)
            self.session.commit()
            self.session.close()
            return {"respuesta": "Producto asociado a rutina alimenticia exitosamente", "token": token}, 200
        self.session.close()
        raise BadRequestError(description="El producto ya se encuentra en la rutina alimenticia")