from src.modelos.pais import Pais, PaisSchema
from src.comandos.base_command import BaseCommand

pais_schema = PaisSchema()

class ObtenerPaises(BaseCommand):
    def __init__(self, session) -> None:
        self.session = session
    
    def execute(self):
        paises = self.session.query(Pais).all()
        return [pais_schema.dump(pais) for pais in paises], 200 