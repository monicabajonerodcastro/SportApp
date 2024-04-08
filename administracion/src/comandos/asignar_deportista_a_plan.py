from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField, NotFoundError, BadRequestError
from src.servicios import auth, http, util
from src.modelos.plan import Plan
from src.modelos.plan_deportistas import PlanDeportistas

from sqlalchemy import and_
import os, uuid

HOST_PERSONAS = os.environ["HOST_PERSONAS"]

class AsignarDeportistaPlan(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.session = session
        self.headers = headers

        auth.validar_autenticacion(self.headers)

        if "id_plan" not in json_request.keys() or json_request["id_plan"] == "":
            raise MissingRequiredField(parameter="Plan Deportivo (id_plan)")

        if "id_deportista" not in json_request.keys() or json_request["id_deportista"] == "":
            raise MissingRequiredField(parameter="Deportista (id_deportista)")
        
        self.id_plan = json_request["id_plan"]
        self.id_deportista = json_request["id_deportista"]
    
    def execute(self):

        # Validar si el plan existe
        if util.is_valid_id(self.id_plan):
            plan = self.session.query(Plan).filter(Plan.id == self.id_plan).first()
            if plan is None:
                raise NotFoundError(description=f"No se encontró un plan con el id [{self.id_plan}]")
        
        # Validar si el deportista existe
        respuesta = http.get_request(url=f"{HOST_PERSONAS}/personas/{self.id_deportista}", headers=self.headers)
        estado_respuesta = respuesta.status_code
        if estado_respuesta == 404:
            raise NotFoundError(description=f"No se encontró un deportista con el id [{self.id_deportista}]")
        if estado_respuesta < 200 or estado_respuesta > 209:
            raise BadRequestError(code=estado_respuesta, description=respuesta.json()["description"])
        
        # Consultar si ya existe una asociación para realizar la actualización
        plan_deportista = self.session.query(PlanDeportistas).filter(
            and_(PlanDeportistas.id_deportista == self.id_deportista, PlanDeportistas.id_plan == self.id_plan)).first()
        
        if plan_deportista is None:
            plan_deportista = PlanDeportistas(id=uuid.uuid4(), id_plan=self.id_plan, id_deportista=self.id_deportista)
        
        plan_deportista.id_plan = self.id_plan
        self.session.add(plan_deportista)
        self.session.commit()

        return {"description": "Deportista asignado correctamente al plan"}, 200