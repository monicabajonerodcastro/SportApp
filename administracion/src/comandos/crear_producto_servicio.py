
import os
from src.modelos.socio import Socio
from src.errores.errores import BadRequestError, InternalServerError, MissingRequiredField, NotFoundError
from src.modelos.producto_servicio import ProductoServicio, ProductoServicioSchema
from src.comandos.base_command import BaseCommand
from src.servicios import auth, util, http

producto_servicio_schema = ProductoServicioSchema()

HOST_DEPORTE = os.environ["HOST_DEPORTE"]

class CrearProductoServicio(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        
        self.session = session
        auth.validar_autenticacion(headers)

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
            response = {}
            try:
                response = http.get_request(f"{HOST_DEPORTE}/deporte/deportes/{id_deporte}")
            except Exception as e:
                raise InternalServerError(description="Ocurrio un error al obtener el deporte, intente más tarde")
            
            if  response.status_code < 200 or response.status_code > 209:
                self.session.close()
                raise NotFoundError(description=f"No se encontró un deporte con el id [{id_deporte}]")
        else:
            self.session.close()
            raise BadRequestError(description="El identificador del deporte no es válido")


        if util.is_valid_id(id_socio):
            socio = self.session.query(Socio).filter(Socio.id == id_socio).first()
            if socio is None:
                self.session.close()
                raise NotFoundError(description=f"No se encontró un Socio con el id [{id_socio}]")
        else:
            self.session.close()
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
        self.session.close()
        return {"description": "Producto o Servicio Registrado con exito"}         
