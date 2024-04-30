
from src.modelos.plan_deportista import PlanDeportista
from src.servicios import auth
from src.comandos.base_command import BaseCommand
from sqlalchemy import and_

class RemoverPlanDeportista(BaseCommand):
    def __init__(self, session, headers, id_plan) -> None:
        self.session = session
        self.headers = headers
        self.id_plan = id_plan

    def execute(self):
        id_deportista = auth.validar_autenticacion(self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(self.headers, retornar_usuario=False)
        plan_deportista = self.session.query(PlanDeportista).filter(and_(PlanDeportista.id_deportista == id_deportista, PlanDeportista.id_plan == self.id_plan)).first()
        self.session.delete(plan_deportista)
        self.session.commit()
        self.session.close()
        return {"respuesta":"Plan desasigado exitosamente", "token": token}, 200