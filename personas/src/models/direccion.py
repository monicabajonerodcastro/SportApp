import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String
from marshmallow import Schema, fields
from src.models.database import Base
from sqlalchemy.orm import relationship

class Direccion(Base):
    __tablename__  =  'direccion'
    id = Column(UUID(as_uuid=True),  default=uuid.uuid4)
    id_direccion = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    ubicacion_latitud = Column(String, nullable=False)
    ubicacion_longitud = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"),primary_key=True)
    
    usuario = relationship("Usuario")

    def __init__(self, id_direccion, direccion, ubicacion_latitud, ubicacion_longitud, nombre, id_usuario):
        self.id_direccion = id_direccion
        self.direccion = direccion
        self.ubicacion_latitud = ubicacion_latitud
        self.ubicacion_longitud = ubicacion_longitud
        self.nombre = nombre
        self.id_usuario = id_usuario

class DireccionSchema(Schema):
    id = fields.Str()
    id_direccion = fields.Str()
    direccion  = fields.Str()
    ubicacion_latitud  = fields.Str()
    ubicacion_longitud = fields.Str()
    nombre = fields.Str()
    id_usuario = fields.Str()
