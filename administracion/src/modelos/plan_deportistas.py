from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.modelos.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
import uuid

class PlanDeportistas(Base):
	__tablename__  =  'plan_deportistas'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	id_deportista = Column(String, nullable=False)
	id_plan = mapped_column(ForeignKey("plan.id"))

	def  __init__(self, id, id_plan, id_deportista):
		self.id = id
		self.id_plan = id_plan
		self.id_deportista = id_deportista

class PlanDeportistasSchema(Schema):
	id = fields.UUID(dump_only=True)
	id_plan  = fields.Str()
	id_deportista  = fields.Str()