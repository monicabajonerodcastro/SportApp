from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from src.modelos.database import Base
from sqlalchemy.orm import relationship

db = SQLAlchemy()
class Evento(Base):
    __tablename__  =  'evento'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    fecha_inicio = Column(db.DateTime(), nullable=False)
    fecha_fin = Column(db.DateTime(), nullable=False)
    id_deporte = Column(String, nullable=False)
    detalle = Column(String, nullable=False)
    id_socio = Column(UUID(as_uuid=True), ForeignKey("socio.id"),primary_key=True, nullable=False)
    socio = relationship("Socio")
    ubicacion = relationship("Ubicacion")

    def  __init__(self, id, nombre, fecha_inicio, fecha_fin, id_deporte, id_socio, detalle):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio  = fecha_inicio
        self.fecha_fin = fecha_fin
        self.id_deporte = id_deporte
        self.id_socio = id_socio
        self.detalle = detalle
class EventoJsonSchema(Schema):
    id = fields.UUID(dump_only=True)
    nombre  = fields.Str()
    fecha_inicio = fields.Str()
    fecha_fin = fields.Str()
    id_deporte = fields.Str()
    id_socio = fields.Str()
    detalle = fields.Str()
