import uuid
from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ProductoAlimenticio(Base):
	__tablename__  =  'producto_alimenticio'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	valor = Column(Integer, nullable=False)
	producto_rutina = relationship('ProductoRutina', backref='producto_alimenticio', lazy=True, uselist=False)

	def __init__(self, nombre, valor):
		self.nombre = nombre
		self.valor = valor

class ProductoAlimenticioSchema(Schema):
	id = fields.UUID(dump_only=True)
	nombre  = fields.Str()
	valor = fields.Int()