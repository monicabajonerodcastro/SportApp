from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Entrenamiento(Base):
	__tablename__  =  'entrenamiento'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	hora_inicio = Column(String, nullable=False)
	hora_fin = Column(String, nullable=False)
	lugar = Column(String, nullable=True)
	detalle = Column(String, nullable=True)
	frecuencia = Column(String, nullable=False)
	deporte = Column(String, nullable=False)

			# Relationships
	#reunion = relationship("Reunion")
	   
	def  __init__(self, nombre, hora_inicio,hora_fin,lugar,detalle,frecuencia,deporte):
		self.nombre  = nombre
		self.hora_inicio = hora_inicio
		self.hora_fin = hora_fin
		self.lugar = lugar
		self.frecuencia = frecuencia
		self.detalle = detalle
		self.deporte = deporte
		
class EntrenadorJsonSchema(Schema):
	id = fields.UUID(dump_only=True)
	nombre  = fields.Str()
	hora_inicio  = fields.Str()
	hora_fin  = fields.Str()
	lugar = fields.Str()
	frecuencia = fields.Str()
	detalle = fields.Str()
	deporte = fields.Str()


