from src.modelos.socio import Socio
from src.comandos.base_command import BaseCommand
from src.errores.errores import MissingRequiredField,InvalidFormatField
from src.servicios import auth
import re


class ActualizarSocio(BaseCommand):
    def __init__(self, session, id, headers, json_request, test ) -> None:
        self.test=test
        self.id=id
        self.headers = headers
        if ( "email" not in json_request.keys() or json_request["email"] =="" or
                "nombre" not in json_request.keys()  or   json_request["nombre"] =="" or
                "apellido" not in json_request.keys() or json_request["apellido"] =="" or
                    "tipo_identificacion" not in json_request.keys() or  json_request["tipo_identificacion"] =="" or
                        "numero_identificacion" not in json_request.keys() or  json_request["numero_identificacion"] =="" or
                            "username" not in json_request.keys() or json_request["username"] =="" or
                                "password" not in json_request.keys() or json_request["password"] =="" or
                                    "detalle" not in json_request.keys() or json_request["detalle"] =="" ) :  
                                    raise MissingRequiredField()


        self.session = session
        self.socio = self.session.query(Socio).filter(Socio.id == self.id).one()
        print(self.socio)
        self.socio.email = json_request["email"]
        self.socio.nombre = json_request["nombre"]
        self.socio.apellido = json_request["apellido"]
        self.socio.tipo_identificacion =  json_request["tipo_identificacion"] if "tipo_identificacion" in json_request.keys() else "" 
        self.socio.numero_identificacion =  json_request["numero_identificacion"] if "numero_identificacion" in json_request.keys() else "" 
        self.socio.username = json_request["username"]
        self.socio.password = json_request["password"]
        self.socio.detalle =  json_request["detalle"] if "detalle" in json_request.keys() else "" 

      
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if(re.fullmatch(regex, self.socio.email) ):
            print(self.socio.email)
        else:
            raise InvalidFormatField    
   
    def execute(self):
        if self.test==False:
            auth.validar_autenticacion(headers=self.headers)
        
        self.session.commit()
        return "Socio Actualizado con exito"
         
