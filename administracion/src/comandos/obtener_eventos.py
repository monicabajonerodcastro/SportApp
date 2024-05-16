import datetime, os, math
from src.modelos.evento_deportista import EventoDeportista, EventoDeportistaJsonSchema
from src.errores.errores import MissingRequiredField
from src.modelos.ubicacion import Ubicacion, UbicacionSchema
from src.modelos.evento import Evento, EventoJsonSchema
from src.comandos.base_command import BaseCommand
from src.servicios import auth, http

HOST_PERSONAS = os.environ["HOST_PERSONAS"]
DISTANCIA_EVENTOS = os.environ["DISTANCIA_EVENTOS"]

evento_schema = EventoJsonSchema()
ubicacion_schema = UbicacionSchema()
evento_deportista_schema = EventoDeportistaJsonSchema()

def _query_eventos_futuros(session):
    return session.query(Evento).filter(Evento.fecha_inicio >= datetime.datetime.now()).order_by(Evento.fecha_inicio.desc()).all()

def _haversine(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad
    
    R = 6371.0 # Radio de la Tierra en kilómetros

    # Fórmula de Haversine
    a = math.sin(d_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distancia en kilómetros
    distance = R * c
    return distance

def _filtrar_eventos_cercanos(session, eventos, usuario_latitud, usuario_longitud):
    respuesta_eventos = []

    for evento in eventos:
        ubicacion = session.query(Ubicacion).filter(Ubicacion.id_evento == evento.id).first()
        if ubicacion is not None:
            evento_latitud = ubicacion.ubicacion_latitud
            evento_longitud = ubicacion.ubicacion_longitud

            distancia = _haversine(float(usuario_latitud), float(usuario_longitud), float(evento_latitud), float(evento_longitud))
            if distancia <= float(DISTANCIA_EVENTOS):
                ubicacion_respuesta = ubicacion_schema.dump(ubicacion)
                evento_respuesta = evento_schema.dump(evento)
                evento_respuesta["ubicacion"] = ubicacion_respuesta
                respuesta_eventos.append(evento_respuesta)   
    return respuesta_eventos   

class ObtenerEventos(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers
       
    def execute(self):
        respuesta_eventos = []
        token = auth.validar_autenticacion(headers=self.headers)
        
        eventos = _query_eventos_futuros(session=self.session)
        for evento in eventos:
            ubicacion = self.session.query(Ubicacion).filter(Ubicacion.id_evento == evento.id).first()
            ubicacion_respuesta = ubicacion_schema.dump(ubicacion)
            evento_respuesta = evento_schema.dump(evento)
            evento_respuesta["ubicacion"] = ubicacion_respuesta
            respuesta_eventos.append(evento_respuesta)
        self.session.close()
        return {"respuesta": respuesta_eventos, "token" : token}, 200
    

class ObtenerEventosCercanos(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers

    def execute(self):
        
        usuario_id = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(headers=self.headers)
        eventos = _query_eventos_futuros(session=self.session)
        respuesta_eventos = _filtrar_eventos_cercanos(self.session, self.headers, eventos, usuario_id)
        self.session.close()
        return {"respuesta": respuesta_eventos, "token" : token}, 200


class ObtenerEventosDeportista(BaseCommand):
    def __init__(self, session, headers) -> None:
        self.session = session
        self.headers = headers

    def execute(self):
        usuario_id = auth.validar_autenticacion(headers=self.headers, retornar_usuario=True)
        token = auth.validar_autenticacion(headers=self.headers)

        eventos_deportista = self.session.query(EventoDeportista).filter(EventoDeportista.id_deportista == usuario_id).all()
        respuesta_eventos_deportista = []
        for evento in eventos_deportista:
            detalle_evento = self.session.query(Evento).filter(Evento.id == evento.id_evento).first()
            evento_dump = evento_schema.dump(detalle_evento)

            ubicacion = self.session.query(Ubicacion).filter(Ubicacion.id_evento == evento.id_evento).first()
            respuesta_ubicacion = ubicacion_schema.dump(ubicacion)
            evento_dump["ubicacion"] = respuesta_ubicacion
            respuesta_eventos_deportista.append(evento_dump)
        return {"respuesta": respuesta_eventos_deportista, "token": token}, 200
    

class ObtenerNuevosEventos(BaseCommand):
    def __init__(self, session, headers, fecha_ultima_conexion, latitud, longitud) -> None:
        self.session = session
        self.headers = headers
        self.fecha_ultima_conexion = fecha_ultima_conexion
        self.latitud = latitud
        self.longitud = longitud
    
    def execute(self):
        if self.latitud == None or self.latitud == "":
            raise MissingRequiredField(description="La latitud es requerida")
        if self.longitud == None or self.longitud == "":
            raise MissingRequiredField(description="La longitud es requerida")
        
        token = auth.validar_autenticacion(headers=self.headers)

        fecha_datetime = datetime.datetime.fromtimestamp(self.fecha_ultima_conexion)
        eventos = self.session.query(Evento).filter(Evento.fecha_creacion >= fecha_datetime).all()
        respuesta_eventos = _filtrar_eventos_cercanos(self.session, eventos, self.latitud, self.longitud) 

        self.session.close()
        return {"respuesta": respuesta_eventos, "token" : token}, 200
