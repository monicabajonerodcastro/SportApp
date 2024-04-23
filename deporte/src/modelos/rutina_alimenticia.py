import uuid
from marshmallow import Schema, fields
from sqlalchemy import Column, String
from src.modelos.producto_rutina import ProductoRutinaSchema
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class RutinaAlimenticia(Base):
	__tablename__  =  'rutina_alimenticia'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	descripcion = Column(String, nullable=False)
	# Relaciones
	productos = relationship("ProductoRutina")

	def __init__(self, nombre, descripcion):
		self.id = uuid.uuid4()
		self.nombre = nombre
		self.descripcion = descripcion

	

class RutinaAlimenticiaSchema(Schema):
	id = fields.UUID(dump_only=True)
	nombre  = fields.Str()
	descripcion  = fields.Str()
	productos = fields.Nested(ProductoRutinaSchema, many=True)