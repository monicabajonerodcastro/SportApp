from src.modelos.plan_entrenamiento import PlanEntrenamiento, PlanEntrenamientoSchema
from src.comandos.base_command import BaseCommand
from src.servicios import auth

plan_entrenamiento_schema = PlanEntrenamientoSchema()

class ObtenerPlanesEntrenamiento(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers
    
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        planes = self.session.query(PlanEntrenamiento).all()
        response = [plan_entrenamiento_schema.dump(plan) for plan in planes]
        self.session.close()
        return {"respuesta": response, "token": nuevo_token}, 200