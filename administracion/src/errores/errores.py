class ApiError(Exception):
    code = 422
    description = "Ocurrió un error general"

class InvalidAuthenticationError(ApiError):
    def __init__(self, code = 401, description= "Usuario y/o contraseña incorrectos"):
        self.code = code
        self.description = description

class NotFoundError(ApiError):
    def __init__(self, code = 404, description= "No se encontró el recurso solicitado"):
        self.code = code
        self.description = description

class BadRequestError(ApiError):
    def __init__(self, code = 400, description= "Ocurrió un error con los datos enviados"):
        self.code = code
        self.description = description

class MissingRequiredToken(ApiError):
    code = 401
    description = "No existe token en la solicitud" 

class MissingRequiredField(ApiError):
    code = 400
    description = "Parámetros requeridos"

class InvalidFormatField(ApiError):
    code = 400
    description = "Parámeto(s) con formato inválido"   

class SocioAlreadyRegistered(ApiError):
    code = 400
    description = "Socio de negocio ya existe" 

class InvalidAuthentication(ApiError):
    def __init__(self, code = 401, description= "Usuario y/o contraseña incorrectos"):
        self.code = code
        self.description = description

