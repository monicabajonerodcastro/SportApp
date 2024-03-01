from src.models.usuario import Usuario
from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredField, MissingRequiredToken,InvalidFormatField
import uuid, re


class CrearUsuario(BaseCommannd):
    def __init__(self, session, json_request, headers) -> None:
        

        if ( "email" not in json_request.keys() or 
                "nombre" not in json_request.keys() or 
                "apellido" not in json_request.keys() or 
                    "deportes_practica" not in json_request.keys()):  
                    raise MissingRequiredField()


        self.session = session
        email = json_request["email"]
        nombre = json_request["nombre"]
        apellido = json_request["apellido"]
        deportes = json_request["deportes_practica"]
        tipo_identificacion =  json_request["tipo_identificacion"] if "tipo_identificacion" in json_request.keys() else "" 
        numero_identificacion =  json_request["numero_identificacion"] if "numero_identificacion" in json_request.keys() else "" 
        genero = json_request["genero"] if "genero" in json_request.keys() else "" 
        fecha_nacimiento = json_request["fecha_nacimiento"] if "fecha_nacimiento" in json_request.keys() else "" 
        peso = json_request["peso"] if "peso" in json_request.keys() else "" 
        altura = json_request["altura"] if "altura" in json_request.keys() else "" 
        pais_nacimiento = json_request["pais_nacimiento"] if "pais_nacimiento" in json_request.keys() else "" 
        ciudad_nacimiento = json_request["ciudad_nacimiento"] if "ciudad_nacimiento" in json_request.keys() else "" 
        antiguedad_residencia = json_request["antiguedad_residencia"] if "antiguedad_residencia" in json_request.keys() else "" 

         
        if email == "" or nombre == "" or apellido == "" or email == "" :
            raise MissingRequiredField

     
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if(re.fullmatch(regex, email) ):
            print(email)
        else:
            raise InvalidFormatField
    
        self.usuario = Usuario(email=email,nombre=nombre, apellido=apellido,
                                tipo_id=tipo_identificacion,
                               	numero_identificacion = numero_identificacion,
                                genero = genero,
                                fecha_nacimiento = fecha_nacimiento,
                                peso = peso,
                                altura = altura,
                                pais_nacimiento = pais_nacimiento,
                                ciudad_nacimiento = ciudad_nacimiento,
                                antiguedad_residencia = antiguedad_residencia,
                                deportes_practica=deportes)
        
   
    def execute(self):
        self.session.add(self.usuario)
        self.session.commit()
        return "Usuario Registrado con exito"
         
