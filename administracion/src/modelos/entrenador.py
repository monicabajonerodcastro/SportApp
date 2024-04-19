from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Entrenador(Base):
	__tablename__  =  'entrenador'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	apellido = Column(String, nullable=False)
	email = Column(String, nullable=False)
	tipo_id = Column(String, nullable=True)
	numero_identificacion = Column(String, nullable=True)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	detalle = Column(String, nullable=False)
	deporte = Column(String, nullable=False)

			# Relationships
	#reunion = relationship("Reunion")
	   
	def  __init__(self, email, nombre, apellido,tipo_id,numero_identificacion,username,password,detalle,deporte):
		self.email  = email
		self.nombre  = nombre
		self.apellido = apellido
		self.tipo_id = tipo_id
		self.numero_identificacion = numero_identificacion
		self.username = username
		self.password = password
		self.detalle = detalle
		self.deporte = deporte
		
class EntrenadorJsonSchema(Schema):
	id = fields.UUID(dump_only=True)
	email  = fields.Str()
	nombre  = fields.Str()
	apellido = fields.Str()
	tipo_id = fields.Str()
	numero_identificacion = fields.Str()
	username = fields.Str()
	detalle = fields.Str()
	deporte = fields.Str()


