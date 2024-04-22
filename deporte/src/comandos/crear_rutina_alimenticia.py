from src.modelos.producto_rutina import ProductoRutina
from src.modelos.rutina_alimenticia import RutinaAlimenticia
from src.errores.errores import MissingRequiredField
from src.comandos.base_command import BaseCommand
from src.servicios import auth

class CrearRutinaAlimenticia(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.session = session
        self.headers = headers

        if "nombre" not in json_request.keys() or json_request["nombre"] == "":
            raise MissingRequiredField(parameter="nombre")
        if "descripcion" not in json_request.keys() or json_request["descripcion"] == "":
            raise MissingRequiredField(parameter="descripcion")
        if "productos" not in json_request.keys() or json_request["productos"] == "" or len(json_request["productos"]) < 1:
            raise MissingRequiredField(parameter="productos")
        
        self.nombre = json_request["nombre"]
        self.descripcion = json_request["descripcion"]
        self.productos = json_request["productos"]
        self.productos_bd = []
            
        self.rutina_alimenticia = RutinaAlimenticia(self.nombre, self.descripcion)

        for prod in self.productos:
            if "producto_id" not in prod.keys() or prod["producto_id"] == "":
                raise MissingRequiredField(parameter="producto_id")
            if "dosis" not in prod.keys() or prod["dosis"] == "":
                raise MissingRequiredField(parameter="dosis")
            self.productos_bd.append(ProductoRutina(producto_id=prod["producto_id"], dosis=prod["dosis"], rutina_alimenticia=self.rutina_alimenticia.id))


    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.rutina_alimenticia)
        self.session.add_all(self.productos_bd)
        self.session.commit()
        self.session.close()
        return {"respuesta": "Rutina alimenticia creada exitosamente", "token": token}, 201