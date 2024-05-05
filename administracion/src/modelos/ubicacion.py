import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String
from marshmallow import Schema, fields
from src.modelos.database import Base
from sqlalchemy.orm import relationship

class Ubicacion(Base):
    __tablename__  =  'ubicacion'
    id = Column(UUID(as_uuid=True),  default=uuid.uuid4)
    id_ubicacion = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    ubicacion_latitud = Column(String, nullable=False)
    ubicacion_longitud = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    id_evento = Column(UUID(as_uuid=True), ForeignKey("evento.id"),primary_key=True)
    
    evento = relationship("Evento")

    def __init__(self, id_ubicacion, direccion, ubicacion_latitud, ubicacion_longitud, nombre, id_evento):
        self.id_ubicacion = id_ubicacion
        self.direccion = direccion
        self.ubicacion_latitud = ubicacion_latitud
        self.ubicacion_longitud = ubicacion_longitud
        self.nombre = nombre
        self.id_evento = id_evento

class UbicacionSchema(Schema):
    id = fields.Str()
    id_ubicacion = fields.Str()
    direccion  = fields.Str()
    ubicacion_latitud  = fields.Str()
    ubicacion_longitud = fields.Str()
    nombre = fields.Str()
    id_evento = fields.Str()
