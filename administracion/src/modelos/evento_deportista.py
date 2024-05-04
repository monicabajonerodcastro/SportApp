from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String
from src.modelos.database import Base


class EventoDeportista(Base):
    __tablename__  =  'evento_deportista'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_deportista = Column(String, nullable=False)
    id_evento = Column(String, nullable=False)

    def  __init__(self, id_evento, id_deportista):
        self.id_deportista = id_deportista
        self.id_evento = id_evento


class EventoDeportistaJsonSchema(Schema):
    id = fields.UUID(dump_only=True)
    id_deportista = fields.Str()
    id_evento  = fields.Str()
