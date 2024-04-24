from src.modelos.deporte import Deporte, DeporteJsonSchema
from src.comandos.base_command import BaseCommand

deporte_schema = DeporteJsonSchema()

class ObtenerDeportes(BaseCommand):
    def __init__(self, session) -> None:
        self.session = session
    
    def execute(self):
        deportes = self.session.query(Deporte).all()
        self.session.close()
        return [deporte_schema.dump(deporte) for deporte in deportes], 200 
    