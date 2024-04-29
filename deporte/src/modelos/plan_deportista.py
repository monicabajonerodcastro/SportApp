import uuid
from marshmallow import Schema, fields
from sqlalchemy import Column, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy  import  Column, ForeignKey

class PlanDeportista(Base):
	__tablename__  =  'plan_deportista'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	id_plan = Column(UUID(as_uuid=True), ForeignKey("plan_entrenamiento.id"),primary_key=True, nullable=False)
	id_deportista = Column(String, nullable=False)
		# Relationships
	plan = relationship("PlanEntrenamiento")

	def __init__(self, id_deportista, id_plan):
		self.id = uuid.uuid4()
		self.id_deportista = id_deportista
		self.id_plan = id_plan

class PlanDeportistaSchema(Schema):
	id = fields.UUID(dump_only=True)
	id_deportista  = fields.Str()
	id_plan  = fields.Str()


    