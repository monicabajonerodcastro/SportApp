class ApiError(Exception):
    code = 422
    description = "An error ocurred"

class MissingRequiredToken(ApiError):
    code = 403
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

