from src.comandos.base_command import BaseCommand
from src.modelos.plan import Plan, PlanSchema
from uuid import UUID

plan_schema = PlanSchema()

class ObtenerPlanId(BaseCommand):
    def __init__(self, session, headers, id_plan) -> None:
        self.session = session
        self.headers = headers
        self.id_plan = id_plan
    
    def _is_valid_id(self, uuid: str, version: int = 4) -> bool:
        try:
            uuid_obj = UUID(uuid, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid

    def execute(self):
        if 'Authorization' not in self.headers:
            return {"mensaje": "No se encontró el header de autorización"}, 403
        else:
            authorization_header = self.headers["Authorization"]
            if "Bearer" not in authorization_header:
                return {"mensaje": "El header de autorización no tiene un formato correcto"}, 403
            # TODO validate token

        if self._is_valid_id(self.id_plan):
            plan = self.session.query(Plan).filter(Plan.id == self.id_plan).first()
            if plan is None:
                return {"mensaje":f"No se encontró un plan con el id [{self.id_plan}]"}, 404

            return plan_schema.dump(plan), 200
        else:
            return {"mensaje": "El identificador del plan no es válido"}, 400
    