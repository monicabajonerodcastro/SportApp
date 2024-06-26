from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.models.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Usuario(Base):
	__tablename__  =  'usuario'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	apellido = Column(String, nullable=False)
	email = Column(String, nullable=False)
	tipo_id = Column(String, nullable=True)
	numero_identificacion = Column(String, nullable=True)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	suscripcion =Column(String, nullable=False)
	rol =  Column(String, nullable=False)
	strava_client_id =Column(String, nullable=True)
	strava_client_secret=Column(String, nullable=True)
	#Relationships
	perfil_deportivo = relationship("PerfilDeportivo")
	direccion = relationship("Direccion")
	    
	def  __init__(self, email, nombre, apellido,tipo_id,numero_identificacion,username,password,suscripcion,rol, strava_client_id=None, strava_client_secret=None):
		self.email  = email
		self.nombre  = nombre
		self.apellido = apellido
		self.tipo_id = tipo_id
		self.numero_identificacion = numero_identificacion
		self.username = username
		self.password = password
		self.suscripcion = suscripcion
		self.rol = rol
		self.strava_client_id = strava_client_id
		self.strava_client_secret = strava_client_secret

class UsuarioJsonSchema(Schema):
	id = fields.UUID(dump_only=True)
	email  = fields.Str()
	nombre  = fields.Str()
	apellido = fields.Str()
	tipo_id = fields.Str()
	numero_identificacion = fields.Str()
	username = fields.Str()
	suscripcion =fields.Str()
	rol = fields.Str()
	strava_client_id = fields.Str()
	strava_client_secret= fields.Str()


