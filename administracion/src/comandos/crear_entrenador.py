from src.modelos.entrenador import Entrenador
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField,InvalidFormatField
from src.servicios import auth
import re

class CrearEntrenador(BaseCommand):
    def __init__(self, session, headers, json_request, test ) -> None:
        self.test=test
        self.headers = headers

        if ( "email" not in json_request.keys() or json_request["email"] =="" or
                "nombre" not in json_request.keys()  or   json_request["nombre"] =="" or
                "apellido" not in json_request.keys() or json_request["apellido"] =="" or
                    "tipo_identificacion" not in json_request.keys() or  json_request["tipo_identificacion"] =="" or
                        "numero_identificacion" not in json_request.keys() or  json_request["numero_identificacion"] =="" or
                            "username" not in json_request.keys() or json_request["username"] =="" or
                                "password" not in json_request.keys() or json_request["password"] =="" or
                                    "detalle" not in json_request.keys() or json_request["detalle"] =="" or
                                        "deporte" not in json_request.keys() or json_request["deporte"] =="" ) :  
                                    raise MissingRequiredField()


        self.session = session
        email = json_request["email"]
        nombre = json_request["nombre"]
        apellido = json_request["apellido"]
        tipo_identificacion =  json_request["tipo_identificacion"] if "tipo_identificacion" in json_request.keys() else "" 
        numero_identificacion =  json_request["numero_identificacion"] if "numero_identificacion" in json_request.keys() else "" 
        username = json_request["username"]
        password = json_request["password"]
        detalle =  json_request["detalle"] if "detalle" in json_request.keys() else "" 
        deporte =  json_request["deporte"]

      
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if(re.fullmatch(regex, email)):
            pass
        else:
            raise InvalidFormatField
    
        self.entrenador = Entrenador(email=email,nombre=nombre, apellido=apellido,
                                tipo_id=tipo_identificacion,
                               	numero_identificacion = numero_identificacion,
                                username = username,
                                password = password,
                                detalle = detalle,
                                deporte=deporte)
        
    def execute(self):
        if self.test==False:
            auth.validar_autenticacion(headers=self.headers)
        self.session.add(self.entrenador)
        self.session.commit()
        return "Entrenador registrado con éxito"
         
