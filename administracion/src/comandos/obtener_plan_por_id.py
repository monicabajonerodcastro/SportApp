from src.comandos.base_command import BaseCommand
from src.modelos.plan import Plan, PlanSchema
from src.servicios import auth, util
from src.errores.errores import NotFoundError, BadRequestError
plan_schema = PlanSchema()


class ObtenerPlanId(BaseCommand):
    def __init__(self, session, headers, id_plan) -> None:
        self.session = session
        self.headers = headers
        self.id_plan = id_plan
       
    def execute(self):
        auth.validar_autenticacion(headers=self.headers)
        
        if util.is_valid_id(self.id_plan):
            plan = self.session.query(Plan).filter(Plan.id == self.id_plan).first()
            if plan is None:
                self.session.close()
                raise NotFoundError(description=f"No se encontró un plan con el id [{self.id_plan}]")
            self.session.close()
            return plan_schema.dump(plan), 200
        else:
            self.session.close()
            raise BadRequestError(description="El identificador del plan no es válido")
    