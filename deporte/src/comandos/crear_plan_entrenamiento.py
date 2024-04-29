from src.modelos.deporte import Deporte
from src.modelos.plan_entrenamiento import PlanEntrenamiento
from src.modelos.plan_entrenamiento_u import PlanEntrenamientoU
from src.modelos.entrenamiento import Entrenamiento
from src.errores.errores import MissingRequiredField, NotFoundError
from src.comandos.base_command import BaseCommand
from src.servicios import auth

class CrearPlanEntrenamiento(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.session = session
        self.headers = headers

        if "nombre" not in json_request.keys() or json_request["nombre"] == "":
            raise MissingRequiredField(parameter="nombre")
        if "id_deporte" not in json_request.keys() or json_request["id_deporte"] == "":
            raise MissingRequiredField(parameter="id_deporte")

        self.nombre = json_request["nombre"]
        self.deporte = json_request["id_deporte"]
        self.entrenamientos = json_request["entrenamientos"]
        self.entrenamientos_bd = []

        deporte = self.session.query(Deporte).filter(Deporte.id == self.deporte).first()
        if deporte is None:
            raise NotFoundError(description="No existe deporte con id "+ self.deporte)

        self.plan_entrenamiento = PlanEntrenamiento(nombre=self.nombre, deporte=self.deporte)

        if self.entrenamientos != '':    
            for entrenamiento in self.entrenamientos:
                entren = self.session.query(Entrenamiento).filter(Entrenamiento.id == entrenamiento).first()
                if entren is None:
                    raise NotFoundError(description="No existe la entrenamiento con id "+ entrenamiento)
                self.entrenamientos_bd.append(PlanEntrenamientoU(id_entrenamiento=entrenamiento, id_plan=self.plan_entrenamiento.id))

    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.plan_entrenamiento)
        self.session.add_all(self.entrenamientos_bd)
        self.session.commit()
        self.session.close()
        return {"description": "Plan de entrenamiento creado exitosamente", "token": token}, 201