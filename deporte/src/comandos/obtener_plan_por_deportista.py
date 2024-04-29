from src.modelos.plan_entrenamiento import PlanEntrenamiento, PlanEntrenamientoSchema
from src.comandos.base_command import BaseCommand
from src.modelos.plan_deportista import PlanDeportista, PlanDeportistaSchema
from src.servicios import auth


plan_deportista_schema = PlanDeportistaSchema()
plan_entrenamiento_schema = PlanEntrenamientoSchema()

class ObtenerPlanesDeportista(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers
        self.planes_deportista = []

    def execute(self):
        id_deportista = auth.validar_autenticacion(self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(self.headers, retornar_usuario=False)
        planes_deportista = self.session.query(PlanDeportista).filter(PlanDeportista.id_deportista == id_deportista).all()
        for plan_deportista in planes_deportista:
            plan_db = self.session.query(PlanEntrenamiento).filter(PlanEntrenamiento.id == plan_deportista.id_plan).first()
            self.planes_deportista.append(plan_entrenamiento_schema.dump(plan_db))

        self.session.close()
        return {"respuesta": self.planes_deportista, "token": token}, 200