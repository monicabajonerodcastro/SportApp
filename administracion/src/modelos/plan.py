from marshmallow import Schema, fields
from sqlalchemy  import  Column, String, Integer
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Plan(Base):
	__tablename__  =  'plan'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	funciones = Column(String, nullable=False)
	valor_mensual = Column(Integer, nullable=False)

	def  __init__(self, id, nombre, funciones, valor_mensual):
		self.id = id
		self.nombre = nombre
		self.funciones = funciones
		self.valor_mensual = valor_mensual

class PlanSchema(Schema):
	id = fields.UUID(dump_only=True)
	nombre  = fields.Str()
	funciones  = fields.Str()
	valor_mensual = fields.Int()