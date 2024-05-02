import enum
import uuid
import datetime
from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime, Numeric
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy  import  Column

class EstadoSesionEntrenamiento(enum.Enum):
    INICIADO = "INICIADO"
    FINALIZADO = "FINALIZADO"


class SesionEntrenamiento(Base):
    __tablename__ = "sesion_entrenamiento"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_deportista = Column(String, nullable=False)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=True)
    estado = Column(String, nullable=False)
    potencia = Column(Numeric, nullable=True)
    min_ritmo = Column(Numeric, nullable=True)
    max_ritmo = Column(Numeric, nullable=True)

    def __init__(self, id_deportista):
        self.id = uuid.uuid4()
        self.id_deportista = id_deportista
        self.hora_inicio = datetime.datetime.now()
        self.hora_fin = None
        self.estado = EstadoSesionEntrenamiento.INICIADO.value

class SesionEntrenamientoSchema(Schema):
    id = fields.UUID(dump_only=True)
    id_deportista = fields.Str()
    hora_inicio = fields.DateTime()
    hora_fin = fields.DateTime()
    estado = fields.Str()
    potencia = fields.Number()
    min_ritmo = fields.Number()
    max_ritmo = fields.Number()