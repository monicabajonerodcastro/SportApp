from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.modelos.database import Base
from sqlalchemy import ForeignKey,Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
import uuid

class ProductoServicio(Base):
	__tablename__  =  'producto_servicio'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	valor = Column(Float, nullable=True,default=0.0)
	detalle = Column(String, nullable=False)
	descripcion = Column(String, nullable=False)
	id_deporte =Column(String, nullable=False)
	id_socio = mapped_column(ForeignKey("socio.id"))

	def  __init__(self, nombre, valor,detalle,descripcion
			   ,id_deporte
	  			,id_socio
			   ):
		self.nombre = nombre
		self.valor = valor
		self.detalle = detalle
		self.descripcion = descripcion
		self.id_deporte = id_deporte
		self.id_socio = id_socio

class ProductoServicioSchema(Schema):
	id = fields.UUID(dump_only=True)
	nombre = fields.Str()
	valor = fields.Str()
	detalle = fields.Str()
	descripcion = fields.Str()
	id_deporte = fields.Str()
	id_socio = fields.Str()