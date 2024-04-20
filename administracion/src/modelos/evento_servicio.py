from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String
from src.modelos.database import Base


class EventoServicio(Base):
    __tablename__  =  'evento_servicio'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_servicio = Column(String, nullable=False)
    id_evento = Column(String, nullable=False)

    def  __init__(self, id_evento, id_servicio):
        self.id_evento = id_evento
        self.id_servicio = id_servicio


class EventoServicioJsonSchema(Schema):
    id = fields.UUID(dump_only=True)
    id_evento  = fields.Str()
    id_servicio = fields.Str()
