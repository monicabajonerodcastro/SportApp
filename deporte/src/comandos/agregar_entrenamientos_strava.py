from src.modelos.entrenamiento import Entrenamiento
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField
from src.servicios import auth

class AgregarEntrenamientosStrava(BaseCommand):
    def __init__(self, session, headers, activities) -> None:
        self.session = session
        self.headers = headers  
        self.activities = activities    
        self.entrenamientos_bd = [] 

        if self.activities == "" or self.activities is None:
            raise MissingRequiredField(parameter="Actividades Strava")

        for entrenamiento in self.activities:       
            nombre = entrenamiento["name"]
            hora_inicio = entrenamiento["start_date"]
            hora_fin =  entrenamiento["start_date"]
            lugar =  entrenamiento["location_country"]
            frecuencia =  "DIARIO"
            detalle =  "Distance: "+str(entrenamiento["distance"])
            deporte =  entrenamiento["type"]

            self.entrenamiento = Entrenamiento(nombre=nombre, hora_inicio=hora_inicio,
                                    hora_fin=hora_fin,
                                    lugar = lugar,
                                    frecuencia = frecuencia,
                                    detalle = detalle,
                                    deporte=deporte)
            
            self.entrenamientos_bd.append(self.entrenamiento)
        
    def execute(self):
        token = auth.validar_autenticacion(headers=self.headers)
        self.session.add_all(self.entrenamientos_bd)
        self.session.commit()
        self.session.close()
        return {"description": "Sincronización de entrenamientos Strava ejecutada correctamente", "token": token}, 201
         

