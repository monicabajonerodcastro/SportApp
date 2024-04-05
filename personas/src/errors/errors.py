class ApiError(Exception):
    code = 422
    description = "An error ocurred"
    

class MissingRequiredToken(ApiError):
    code = 401
    description = "No existe token en la solicitud" 

class MissingRequiredField(ApiError):
    code = 400
    description = "Parámetros requeridos"

class InvalidFormatField(ApiError):
    code = 400
    description = "Parámeto(s) con formato inválido"   

class InvalidUser(ApiError):
    code = 400
    description = "Usuario no existe" 

class PerfilDeportivoAlreadyRegistered(ApiError):
    code = 400
    description = "Perfil Deportivo ya existe" 

class InvalidAuthentication(ApiError):
    def __init__(self, code = 401, description= "Usuario y/o contraseña incorrectos"):
        self.code = code
        self.description = description

class NotFoundError(ApiError):
    def __init__(self, code = 404, description= "No se encontró el recurso solicitado"):
        self.code = code
        self.description = description
