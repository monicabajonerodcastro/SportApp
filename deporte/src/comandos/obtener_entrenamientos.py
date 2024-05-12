from src.errores.errores import NotFoundError
from src.modelos.entrenamiento import Entrenamiento, EntrenadorJsonSchema
from src.comandos.base_command import BaseCommand
from src.servicios import auth

entrenamiento_schema = EntrenadorJsonSchema()

class ObtenerEntrenamientos(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers
    
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        entrenamientos = self.session.query(Entrenamiento).all()
        response = [entrenamiento_schema.dump(entrenamiento) for entrenamiento in entrenamientos]
        self.session.close()
        return {"entrenamientos": response, "token": nuevo_token}, 200
class ObtenerEntrenamientoPorId(BaseCommand):
    def __init__(self, session, id_entrenamiento) -> None:
        self.session = session
        self.id_entrenamiento = id_entrenamiento
    
    def execute(self):
        entrenamiento = self.session.query(Entrenamiento).filter(Entrenamiento.id == self.id_entrenamiento).first()
        self.session.close()
        if entrenamiento is None:
            raise NotFoundError(description="No se encontró un deporte con el id " + self.id_deporte)
        return entrenamiento_schema.dump(entrenamiento) 