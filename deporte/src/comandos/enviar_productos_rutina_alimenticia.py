import datetime
from enum import Enum
import enum
import os
from src.modelos.envio_productos_rutina import EnvioProductosRutina
from src.servicios import auth, http, pub_sub
from src.errores.errores import BadRequestError, NotFoundError
from src.modelos.rutina_alimenticia import RutinaAlimenticia
from src.comandos.base_command import BaseCommand

HOST_PERSONAS = os.environ["HOST_PERSONAS"]
PROJECT_ID = os.environ["PROJECT_ID"]
TOPIC_ENVIO_PRODUCTOS = os.environ["TOPIC_ENVIO_PRODUCTOS"]

class EstadoEnvio(Enum):
    CREADO = "CREADO"
    ENVIADO = "ENVIADO"
    ENTREGADO = "ENTREGADO"
    DEVUELTO = "DEVUELTO"

class EnviarProductosRutinaAlimenticia(BaseCommand):
    def __init__(self, session, headers, id_rutina_alimenticia) -> None:
        self.session = session
        self.headers = headers
        self.id_rutina_alimenticia = id_rutina_alimenticia
    
    def _validar_rutina_alimenticia(self):
        rutina_alimenticia: RutinaAlimenticia = self.session.query(RutinaAlimenticia).filter(RutinaAlimenticia.id == self.id_rutina_alimenticia).first()
        if rutina_alimenticia is None:
            raise NotFoundError(description=f"No existe la rutina alimenticia con id [{self.id_rutina_alimenticia}]")

    def execute(self):
        self._validar_rutina_alimenticia()
        
        fecha_hoy = datetime.datetime.now()
        fecha_mas_uno = fecha_hoy + datetime.timedelta(days=1)
        fecha_mas_cinco = fecha_mas_uno + datetime.timedelta(days=5)

        envio_productos_rutina = EnvioProductosRutina(id_rutina=self.id_rutina_alimenticia, id_deportista="", direccion="",
                                                      nombre_deportista="", fecha_creacion=fecha_hoy, 
                                                      fecha_envio=fecha_mas_uno, fecha_entrega=fecha_mas_cinco, estado = EstadoEnvio.CREADO.value)
        self.session.add(envio_productos_rutina)
        self.session.commit()

        publicador = pub_sub.PublicadorMensajes(project_id=PROJECT_ID, topic_id=TOPIC_ENVIO_PRODUCTOS)
        publicador.publicar_mensaje(envio_productos_rutina.as_dict())
        self.session.close()

        return {"respuesta": "Solicitud de productos enviada exitosamente. De 5 a 8 días recibirá sus productos"}, 200

