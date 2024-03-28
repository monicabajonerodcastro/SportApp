
from src.comandos.base_command import BaseCommand
from src.modelos.plan import Plan, PlanSchema

plan_schema = PlanSchema()

class ObtenerPlan(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers

    def execute(self):
        if 'Authorization' not in self.headers:
            return {"mensaje": "No se encontró el header de autorización"}, 403
        else:
            authorization_header = self.headers["Authorization"]
            if "Bearer" not in authorization_header:
                return {"mensaje": "El header de autorización no tiene un formato correcto"}, 403
            # TODO validate token

        planes = self.session.query(Plan).all() 
        return [plan_schema.dump(plan) for plan in planes], 200 
    