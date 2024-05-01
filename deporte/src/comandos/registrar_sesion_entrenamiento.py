import datetime
from src.errores.errores import NotFoundError
from src.modelos.sesion_entrenamiento import EstadoSesionEntrenamiento, SesionEntrenamiento
from src.comandos.base_command import BaseCommand
from src.servicios import auth

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
    def __init__(self, session, headers, id_sesion_entrenamiento) -> None:
        self.session = session
        self.headers = headers
        self.id_sesion_entrenamiento = id_sesion_entrenamiento

    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        sesion_entrenamiento = self.session.query(SesionEntrenamiento).filter(SesionEntrenamiento.id == self.id_sesion_entrenamiento).first()
        if sesion_entrenamiento is None:
            raise NotFoundError(description="No se ha iniciado la sesión de entrenamiento " + self.id_sesion_entrenamiento)
        sesion_entrenamiento.hora_fin = datetime.datetime.now()
        sesion_entrenamiento.estado = EstadoSesionEntrenamiento.FINALIZADO.value
        self.session.add(sesion_entrenamiento)
        self.session.commit()
        self.session.close()
        return {"respuesta": "Sesión de entrenamiento finalizada exitosamente", "id_sesion_entrenamiento": self.id_sesion_entrenamiento, "token": nuevo_token}, 200