import uuid
from marshmallow import Schema, fields
from sqlalchemy import Column, Date, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID


class EnvioProductosRutina(Base):
	__tablename__  =  'envio_productos_rutina'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	id_rutina = Column(String, nullable=False)
	id_deportista = Column(String, nullable=False)
	nombre_deportista = Column(String, nullable=False)
	direccion = Column(String, nullable=False)
	fecha_creacion = Column(Date, nullable=False)
	fecha_envio = Column(Date, nullable=False)
	fecha_entrega = Column(Date, nullable=False)
	estado = Column(String, nullable=False)

	def __init__(self, id_rutina, id_deportista, direccion, nombre_deportista, fecha_creacion, fecha_envio, fecha_entrega, estado):
		self.id_rutina = id_rutina
		self.id_deportista = id_deportista
		self.direccion = direccion
		self.nombre_deportista = nombre_deportista
		self.fecha_creacion = fecha_creacion
		self.fecha_envio = fecha_envio
		self.fecha_entrega = fecha_entrega
		self.estado = estado
	
	def as_dict(self) -> str:
		return (
			"{'id_rutina': '" + self.id_rutina 
			+ "', 'id_deportista': '"+ self.id_deportista 
			+ "', 'direccion': '"+ self.direccion 
			+ "', 'nombre_deportista': '"+ self.nombre_deportista 
			+ "', 'fecha_creacion': '"+ (self.fecha_creacion.strftime("%Y") + "-" + self.fecha_creacion.strftime("%m") + "-" + self.fecha_creacion.strftime("%d"))
			+ "', 'fecha_envio': '"+ (self.fecha_envio.strftime("%Y") + "-" + self.fecha_envio.strftime("%m") + "-" + self.fecha_envio.strftime("%d"))
			+ "', 'fecha_entrega': '"+ (self.fecha_entrega.strftime("%Y") + "-" + self.fecha_entrega.strftime("%m") + "-" + self.fecha_entrega.strftime("%d"))
			+ "', 'estado': '"+ self.estado
			+ "'}"
		)

class ProductoAlimenticioSchema(Schema):
	id = fields.UUID(dump_only=True)
	id_rutina = fields.Str()
	id_deportista = fields.Str()
	direccion = fields.Str()
	nombre_deportista = fields.Str()
	fecha_creacion = fields.Date()
	fecha_envio = fields.Date()
	fecha_entrega = fields.Date()
	estado = Column(String, nullable=False)
	