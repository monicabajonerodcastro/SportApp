
from src.comandos.base_command import BaseCommand
from src.modelos.plan import Plan, PlanSchema
from src.servicios import auth

plan_schema = PlanSchema()

class ObtenerPlan(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers

    def execute(self):
        auth.validar_autenticacion(headers=self.headers)

        planes = self.session.query(Plan).all() 
        return [plan_schema.dump(plan) for plan in planes], 200 
    