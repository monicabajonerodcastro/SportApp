from src.modelos.producto_alimenticio import ProductoAlimenticio
from src.errores.errores import MissingRequiredField
from src.comandos.base_command import BaseCommand
from src.servicios import auth

class CrearProductoAlimenticio(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.session = session
        self.headers = headers

        if "nombre" not in json_request.keys() or json_request["nombre"] == "":
            raise MissingRequiredField(parameter="nombre")
        if "valor" not in json_request.keys() or json_request["valor"] == "":
            raise MissingRequiredField(parameter="valor")
          
        self.nombre = json_request["nombre"]
        self.valor = json_request["valor"]

        self.producto_alimenticio = ProductoAlimenticio(self.nombre, self.valor)

    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.producto_alimenticio)
        self.session.commit()
        self.session.close()
        return {"respuesta": "Producto alimenticio creado exitosamente", "token": token}, 201