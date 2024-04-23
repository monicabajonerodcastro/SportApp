import uuid
from marshmallow import Schema, fields
from sqlalchemy import Column, ForeignKey, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID


class ProductoRutina(Base):
	__tablename__  =  'producto_rutina'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	dosis = Column(String, nullable=False)
	# Relaciones
	producto_id = Column(UUID(as_uuid=True), ForeignKey("producto_alimenticio.id"), nullable=False)
	rutina_alimenticia = Column(UUID(as_uuid=True), ForeignKey("rutina_alimenticia.id"))
	
	def __init__(self, producto_id, dosis, rutina_alimenticia):
		self.dosis = dosis
		self.producto_id = producto_id
		self.rutina_alimenticia = rutina_alimenticia


class ProductoRutinaSchema(Schema):
	id = fields.UUID(dump_only=True)
	dosis = fields.Str()
	producto_id = fields.Str()
	rutina_alimenticia_id = fields.Str()