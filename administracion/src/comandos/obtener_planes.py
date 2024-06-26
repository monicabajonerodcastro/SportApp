
from src.comandos.base_command import BaseCommand
from src.modelos.plan import Plan, PlanSchema
from src.servicios import auth

plan_schema = PlanSchema()

class ObtenerPlan(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers

    def execute(self):
        planes = self.session.query(Plan).all() 
        self.session.close()
        return [plan_schema.dump(plan) for plan in planes], 200 
    