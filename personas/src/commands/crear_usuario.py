from src.models.usuario import Usuario
from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredField,InvalidFormatField
import re


class CrearUsuario(BaseCommannd):

    def _validar_campo(self, campo, json, mensaje) -> None:
        if campo in json and json[campo] != "" and json[campo] != None:
            return json[campo]
        raise MissingRequiredField(description=mensaje)
    
    def __init__(self, session, json_request) -> None:
        self.session = session
        email = self._validar_campo("email", json_request, "No se encontró el email en la petición")
        nombre = self._validar_campo("nombre", json_request, "No se encontró el nombre en la petición")
        apellido = self._validar_campo("apellido", json_request, "No se encontró el apellido en la petición")
        tipo_identificacion = self._validar_campo("tipo_identificacion", json_request, "No se encontró el tipo de identificacion en la petición")
        numero_identificacion = self._validar_campo("numero_identificacion", json_request, "No se encontró el numero de identificacion en la petición")
        username = self._validar_campo("username", json_request, "No se encontró el username en la petición")
        password = self._validar_campo("password", json_request, "No se encontró el password en la petición")
        suscripcion = self._validar_campo("suscripcion", json_request, "No se encontró la suscripcion en la petición")
      
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if(re.fullmatch(regex, email) ):
            print(email)
        else:
            raise InvalidFormatField(description="El correo no tiene un formato válido")
    
        self.usuario = Usuario(email=email,nombre=nombre, apellido=apellido,
                                tipo_id=tipo_identificacion,
                               	numero_identificacion = numero_identificacion,
                                username = username,
                                password = password,
                                suscripcion = suscripcion, rol="DEPORTISTA")
        
   
    def execute(self):
        self.session.add(self.usuario)
        self.session.commit()
        self.session.close()
        return {"description" : "Usuario Registrado con exito", "id": self.usuario.id}
         
