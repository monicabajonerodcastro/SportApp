from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Deporte(Base):
	__tablename__  =  'deporte'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	
	
    
	def  __init__(self, nombre):
		self.nombre  = nombre

		


class DeporteJsonSchema(Schema):
	id = fields.UUID(dump_only=True)
	nombre  = fields.Str()

