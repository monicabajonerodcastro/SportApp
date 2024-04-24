from src.errores.errores import NotFoundError
from src.modelos.deporte import Deporte, DeporteJsonSchema
from src.comandos.base_command import BaseCommand

deporte_schema = DeporteJsonSchema()

class ObtenerDeportePorId(BaseCommand):
    def __init__(self, session, id_deporte) -> None:
        self.session = session
        self.id_deporte = id_deporte
    
    def execute(self):
        deporte = self.session.query(Deporte).filter(Deporte.id == self.id_deporte).first()
        self.session.close()
        if deporte is None:
            raise NotFoundError(description="No se encontró un deporte con el id " + self.id_deporte)
        return deporte_schema.dump(deporte), 200 
    