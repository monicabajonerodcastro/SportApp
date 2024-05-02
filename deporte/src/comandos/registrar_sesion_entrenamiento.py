import datetime
from src.errores.errores import MissingRequiredField, NotFoundError
from src.modelos.sesion_entrenamiento import EstadoSesionEntrenamiento, SesionEntrenamiento
from src.comandos.base_command import BaseCommand
from src.servicios import auth

def _validar_campo(campo, json, mensaje) -> None:
    if campo in json and json[campo] != "" and json[campo] != None:
        return json[campo]
    raise MissingRequiredField(description=mensaje)
        

class IniciarSesionEntrenamiento(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers

    def execute(self):
        deportista_id = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True)
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        sesion_entrenamiento = SesionEntrenamiento(deportista_id)
        sesion_entrenamiento_id = sesion_entrenamiento.id
        self.session.add(sesion_entrenamiento)
        self.session.commit()
        self.session.close()
        return {"respuesta": "Sesión de entrenamiento iniciada exitosamente", "id_sesion_entrenamiento": sesion_entrenamiento_id, "token": nuevo_token}, 201
    
class FinalizarSesionEntrenamiento(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.session = session
        self.headers = headers

        self.id_sesion_entrenamiento = _validar_campo("id_sesion_entrenamiento", json_request, "No se encontró el id de la sesión de entrenamiento")
        self.potencia = _validar_campo("potencia", json_request, "No se encontró la potencia")
        self.min_ritmo = _validar_campo("min_ritmo", json_request, "No se encontró el ritmo cardiaco mínimo")
        self.max_ritmo = _validar_campo("max_ritmo", json_request, "No se encontró el ritmo cardiaco máximo")

    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        sesion_entrenamiento = self.session.query(SesionEntrenamiento).filter(SesionEntrenamiento.id == self.id_sesion_entrenamiento).first()
        if sesion_entrenamiento is None:
            raise NotFoundError(description="No se ha iniciado la sesión de entrenamiento " + self.id_sesion_entrenamiento)
        sesion_entrenamiento.hora_fin = datetime.datetime.now()
        sesion_entrenamiento.estado = EstadoSesionEntrenamiento.FINALIZADO.value
        sesion_entrenamiento.potencia = self.potencia
        sesion_entrenamiento.min_ritmo = self.min_ritmo
        sesion_entrenamiento.max_ritmo = self.max_ritmo
        self.session.add(sesion_entrenamiento)
        self.session.commit()
        self.session.close()
        return {"respuesta": "Sesión de entrenamiento finalizada exitosamente", "id_sesion_entrenamiento": self.id_sesion_entrenamiento, "token": nuevo_token}, 200