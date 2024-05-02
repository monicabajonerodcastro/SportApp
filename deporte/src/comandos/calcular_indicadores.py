import datetime

from sqlalchemy import and_
from src.modelos.sesion_entrenamiento import SesionEntrenamiento, EstadoSesionEntrenamiento
from src.servicios import auth
from src.comandos.base_command import BaseCommand

class CalcularIndicadores(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers

    def calcular_ftp(self, hora_inicio: datetime.datetime, hora_fin: datetime.datetime, potencia: str):
        minutos_entrenamiento = ((hora_fin - hora_inicio).total_seconds())/60
        if minutos_entrenamiento < 8:
            return round(float(potencia) * 0.8, 2)
        elif minutos_entrenamiento < 20:
            return round(float(potencia) * 0.9, 2)
        else:
            return round(float(potencia) * 0.95, 2)
        
    def calculate_vo2max(self, min_ritmo: str, max_ritmo: str):
        return round(15 * ( float(max_ritmo)/float(min_ritmo)))
            
    def execute(self):
        id_deportista = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(headers=self.headers)

        respuesta = []
        sesiones_entrenamiento = self.session.query(SesionEntrenamiento).filter(and_(SesionEntrenamiento.id_deportista == id_deportista, SesionEntrenamiento.estado == EstadoSesionEntrenamiento.FINALIZADO.value)).order_by(SesionEntrenamiento.hora_inicio.desc()).all()
        for sesion in sesiones_entrenamiento:
            respuesta.append({
                "fecha": sesion.hora_inicio.strftime("%m/%d/%Y %I:%M:%S %p"),
                "ftp": self.calcular_ftp(sesion.hora_inicio, sesion.hora_fin, sesion.potencia),
                "vo2max": self.calculate_vo2max(sesion.min_ritmo, sesion.max_ritmo)
            })
        return {"respuesta": respuesta, "token": token}, 200
