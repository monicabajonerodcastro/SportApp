from src.comandos.base_command import BaseCommand
from src.modelos.plan import Plan, PlanSchema
from src.servicios import auth
from uuid import UUID
from src.errores.errores import NotFoundError, BadRequestError
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
        auth.validar_autenticacion(headers=self.headers)
        
        if self._is_valid_id(self.id_plan):
            plan = self.session.query(Plan).filter(Plan.id == self.id_plan).first()
            if plan is None:
                raise NotFoundError(description=f"No se encontró un plan con el id [{self.id_plan}]")

            return plan_schema.dump(plan), 200
        else:
            raise BadRequestError(description="El identificador del plan no es válido")
    