from src.models.usuario import Usuario
from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredField,InvalidFormatField
import re


class CrearUsuario(BaseCommannd):
    def __init__(self, session, json_request) -> None:
        

        if ( "email" not in json_request.keys() or json_request["email"] =="" or
                "nombre" not in json_request.keys()  or   json_request["nombre"] =="" or
                "apellido" not in json_request.keys() or json_request["apellido"] =="" or
                    "tipo_identificacion" not in json_request.keys() or  json_request["tipo_identificacion"] =="" or
                        "numero_identificacion" not in json_request.keys() or  json_request["numero_identificacion"] =="" or
                            "username" not in json_request.keys() or json_request["username"] =="" or
                                "password" not in json_request.keys() or json_request["password"] =="" or
                                    "suscripcion" not in json_request.keys() or json_request["suscripcion"] =="" ) :  
                                    raise MissingRequiredField()


        self.session = session
        email = json_request["email"]
        nombre = json_request["nombre"]
        apellido = json_request["apellido"]
        tipo_identificacion =  json_request["tipo_identificacion"] if "tipo_identificacion" in json_request.keys() else "" 
        numero_identificacion =  json_request["numero_identificacion"] if "numero_identificacion" in json_request.keys() else "" 
        username = json_request["username"]
        password = json_request["password"]
        suscripcion =  json_request["suscripcion"] if "suscripcion" in json_request.keys() else "" 

      
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if(re.fullmatch(regex, email) ):
            print(email)
        else:
            raise InvalidFormatField
    
        self.usuario = Usuario(email=email,nombre=nombre, apellido=apellido,
                                tipo_id=tipo_identificacion,
                               	numero_identificacion = numero_identificacion,
                                username = username,
                                password = password,
                                suscripcion = suscripcion, rol="DEPORTISTA")
        
   
    def execute(self):
        self.session.add(self.usuario)
        self.session.commit()
        return "Usuario Registrado con exito"
         
