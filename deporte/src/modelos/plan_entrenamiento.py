import uuid
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PlanEntrenamiento(Base):
	__tablename__  =  'plan_entrenamiento'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	id_deporte = Column(UUID(as_uuid=True), ForeignKey("deporte.id"), primary_key=True, nullable=True)
	
	deporte = relationship("Deporte")

	def __init__(self, nombre, deporte):
		self.id = uuid.uuid4()
		self.nombre = nombre
		self.id_deporte = deporte

class PlanEntrenamientoSchema(Schema):
	id = fields.UUID(dump_only=True)
	nombre  = fields.Str()
	id_deporte  = fields.UUID(dump_only=True)
