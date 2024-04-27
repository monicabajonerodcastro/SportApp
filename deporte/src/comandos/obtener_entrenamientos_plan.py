
from sqlalchemy import JSON
from src.modelos.entrenamiento import Entrenamiento, EntrenadorJsonSchema
from src.comandos.base_command import BaseCommand
from src.modelos.plan_entrenamiento_u import PlanEntrenamientoU
from src.servicios import auth

entrenmiento_schema = EntrenadorJsonSchema()

class ObtenerEntrenamientosPlan(BaseCommand):
    def __init__(self, session, id_plan, headers):
        self.session = session
        self.headers = headers
        self.id_plan = id_plan
        
        self.entrenamientos = session.query(Entrenamiento).join(PlanEntrenamientoU).filter(PlanEntrenamientoU.id_plan == id_plan).all() 
 
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        respuesta = [entrenmiento_schema.dump(entrenamiento) for entrenamiento in self.entrenamientos]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200
    