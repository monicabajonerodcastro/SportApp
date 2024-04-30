from src.modelos.plan_deportista import PlanDeportista
from src.servicios import auth
from src.comandos.base_command import BaseCommand

class AsignarPlanDeportista(BaseCommand):
    def __init__(self, session, headers, id_plan) -> None:
       self.session = session
       self.headers = headers
       self.id_plan = id_plan
    
    def execute(self):
        id_deportista = auth.validar_autenticacion(self.headers, retornar_usuario=True)
        plan_deportista = PlanDeportista(id_deportista=id_deportista, id_plan=self.id_plan)
        self.session.add(plan_deportista)
        self.session.commit()
        self.session.close()
        return {"description": "Plan de entrenamiento asociado al deportista exitosamente"}, 201


    