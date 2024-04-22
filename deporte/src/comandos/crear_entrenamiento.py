from src.modelos.entrenamiento import Entrenamiento
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField
from src.servicios import auth

class CrearEntrenamiento(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.headers = headers       

        if "nombre" not in json_request.keys() or json_request["nombre"] == "":
            raise MissingRequiredField(parameter="Entrenamiento (nombre)")
        if "hora_inicio" not in json_request.keys() or json_request["hora_inicio"] == "":
            raise MissingRequiredField(parameter="Entrenamiento (hora_inicio)")
        if "hora_fin" not in json_request.keys() or json_request["hora_fin"] == "":
            raise MissingRequiredField(parameter="Entrenamiento (hora_fin)")
        if "lugar" not in json_request.keys() or json_request["lugar"] == "":
            raise MissingRequiredField(parameter="Entrenamiento (lugar)")
        if "frecuencia" not in json_request.keys() or json_request["frecuencia"] == "":
            raise MissingRequiredField(parameter="Entrenamiento (frecuencia)")
        if "detalle" not in json_request.keys() or json_request["detalle"] == "":
            raise MissingRequiredField(parameter="Entrenamiento (detalle)")
        if "deporte" not in json_request.keys() or json_request["deporte"] == "":
            raise MissingRequiredField(parameter="Entrenamiento (deporte)")


        self.session = session
        nombre = json_request["nombre"]
        hora_inicio = json_request["hora_inicio"]
        hora_fin =  json_request["hora_fin"] if "hora_fin" in json_request.keys() else ""
        lugar =  json_request["lugar"] if "lugar" in json_request.keys() else ""
        frecuencia =  json_request["frecuencia"] if "frecuencia" in json_request.keys() else ""
        detalle =  json_request["detalle"] if "detalle" in json_request.keys() else ""
        deporte =  json_request["deporte"]

    
        self.entrenamiento = Entrenamiento(nombre=nombre, hora_inicio=hora_inicio,
                                hora_fin=hora_fin,
                               	lugar = lugar,
                                frecuencia = frecuencia,
                                detalle = detalle,
                                deporte=deporte)
        
    def execute(self):
        auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.entrenamiento)
        self.session.commit()
        self.session.close()
        return "Entrenamiento registrado con éxito"
         
