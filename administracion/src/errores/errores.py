class ApiError(Exception):
    code = 422
    description = "Ocurrió un error general"