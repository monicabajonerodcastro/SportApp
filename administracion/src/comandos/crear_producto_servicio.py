
from src.modelos.socio import Socio
from src.modelos.deporte import Deporte
from src.errores.errores import BadRequestError, MissingRequiredField, NotFoundError
from src.modelos.producto_servicio import ProductoServicio, ProductoServicioSchema
from src.comandos.base_command import BaseCommand
from src.servicios import auth, util

producto_servicio_schema = ProductoServicioSchema()


class CrearProductoServicio(BaseCommand):
    def __init__(self, session, json_request) -> None:
        
        self.session = session


        if "nombre" not in json_request.keys() or json_request["nombre"] == "":
            raise MissingRequiredField(parameter="Producto Servicio (nombre)")
        if "valor" not in json_request.keys() or json_request["valor"] == "":
            raise MissingRequiredField(parameter="Producto Servicio (valor)")
        if "detalle" not in json_request.keys() or json_request["detalle"] == "":
            raise MissingRequiredField(parameter="Producto Servicio (detalle)")
        if "descripcion" not in json_request.keys() or json_request["descripcion"] == "":
            raise MissingRequiredField(parameter="Producto Servicio (descripcion)")
        if "id_deporte" not in json_request.keys() or json_request["id_deporte"] == "":
            raise MissingRequiredField(parameter="Producto Servicio (id_deporte)")
        if "id_socio" not in json_request.keys() or json_request["id_socio"] == "":
            raise MissingRequiredField(parameter="Producto Servicio (id_socio)")
        

        nombre = json_request["nombre"]
        valor = json_request["valor"]
        detalle = json_request["detalle"]
        descripcion = json_request["descripcion"]
        id_deporte =  json_request["id_deporte"] 
        id_socio =  json_request["id_socio"] 

        if util.is_valid_id(id_deporte):
            deporte = self.session.query(Deporte).filter(Deporte.id == id_deporte).first()
            if deporte is None:
                raise NotFoundError(description=f"No se encontró un Deporte con el id [{id_deporte}]")
        else:
            raise BadRequestError(description="El identificador del Deporte no es válido")


        if util.is_valid_id(id_socio):
            socio = self.session.query(Socio).filter(Socio.id == id_socio).first()
            if socio is None:
                raise NotFoundError(description=f"No se encontró un Socio con el id [{id_socio}]")
        else:
            raise BadRequestError(description="El identificador del Socio no es válido")

    
        self.producto_servicio = ProductoServicio(
                        nombre = nombre,
                        valor = valor,
                        detalle = detalle,
                        descripcion = descripcion,
                        id_deporte =  id_deporte,
                        id_socio =  id_socio 
                    )
        
   
    def execute(self):
        self.session.add(self.producto_servicio)
        self.session.commit()
        return {"description": "Producto o Servicio Registrado con exito"}         
