import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String
from marshmallow import Schema, fields
from src.models.database import Base

class InicioSesion(Base):
    __tablename__  =  'inicio_sesion'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = Column(UUID(as_uuid=True), nullable=False)
    ultima_conexion = Column(DateTime, nullable=False)
    
    def __init__(self, id_usuario, ultima_conexion):
        self.id_usuario = id_usuario
        self.ultima_conexion = ultima_conexion

class InicioSesionSchema(Schema):
    id = fields.Str()
    id_usuario = fields.Str()
    ultima_conexion = fields.DateTime()
