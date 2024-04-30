from src.modelos.ciudad import Ciudad, CiudadSchema
from src.comandos.base_command import BaseCommand

ciudad_schema = CiudadSchema()

class ObtenerCiudades(BaseCommand):
    def __init__(self, session, id_pais) -> None:
        self.session = session
        self.id_pais = id_pais
    
    def execute(self):
        ciudades = self.session.query(Ciudad).filter(Ciudad.pais == self.id_pais).all()
        self.session.close()
        return [ciudad_schema.dump(ciudad) for ciudad in ciudades], 200 