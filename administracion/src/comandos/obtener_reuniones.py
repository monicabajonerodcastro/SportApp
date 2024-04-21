
from sqlalchemy import JSON
from src.modelos.entrenador import Entrenador
from src.comandos.base_command import BaseCommand
from src.modelos.reunion import Reunion, ReunionJsonSchema, ReunionDisponibleJsonSchema
from src.servicios import auth
import datetime

reunion_schema = ReunionJsonSchema()
reunion_disponible_schema = ReunionDisponibleJsonSchema()

class ObtenerReuniones(BaseCommand):
    def __init__(self, session, headers):
        self.session = session
        self.headers = headers
        
    
    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)

        self.reuniones = self.session.query(Reunion).all()
        respuesta = [reunion_schema.dump(reunion) for reunion in self.reuniones]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200
    
class ObteneReunionesDisponibles(BaseCommand):
    def __init__(self, session, headers):

        self.session = session
        self.headers = headers

        self.reuniones = session.query(Reunion).join(Entrenador).filter(Reunion.id_usuario == None).order_by(Reunion.fecha.desc()).all() 
        for reunion in self.reuniones:

            reunion.nombre_entrenador=reunion.entrenador.nombre+" "+reunion.entrenador.apellido
            reunion.detalle_entrenador=reunion.entrenador.detalle
            reunion.fecha=reunion.fecha.strftime('%d/%m/%y %H:%M')

    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        respuesta = [reunion_disponible_schema.dump(reunion) for reunion in self.reuniones]
        self.session.close()
        return {"respuesta": respuesta, "token": nuevo_token}, 200
    
    