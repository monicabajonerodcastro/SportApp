import uuid
from marshmallow import Schema, fields
from sqlalchemy import UUID, Column, String
from src.modelos.database import Base


class ServicioDeportista(Base):
    __tablename__  =  'servicio_deportista'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_servicio = Column(String, nullable=False)
    id_deportista = Column(String, nullable=False)

    def __init__(self, id_servicio, id_deportista):
        self.id_servicio = id_servicio
        self.id_deportista = id_deportista

class ServicioDeportistaJsonSchema(Schema):

	id = fields.UUID(dump_only=True)
	id_servicio  = fields.Str()
	id_deportista  = fields.Str()
