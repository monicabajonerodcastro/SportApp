
from src.comandos.base_command import BaseCommand
from src.modelos.producto_servicio import ProductoServicio, ProductoServicioSchema
from src.servicios import auth

producto_servicio_schema = ProductoServicioSchema()

class ObtenerProductoServicios(BaseCommand):
    def __init__(self, session):
        self.session = session
        
    
    def execute(self):
 
        self.producto_servicio = self.session.query(ProductoServicio).all() 
        return [producto_servicio_schema.dump(ps) for ps in self.producto_servicio], 200  


