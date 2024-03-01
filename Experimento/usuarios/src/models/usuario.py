from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.models.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Usuario(Base):
	__tablename__  =  'usuario'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nombre = Column(String, nullable=False)
	apellido = Column(String, nullable=False)
	email = Column(String, nullable=False)
	tipo_id = Column(String, nullable=True)
	numero_identificacion = Column(String, nullable=True)
	genero = Column(String, nullable=True)
	fecha_nacimiento = Column(String, nullable=True)
	peso = Column(String, nullable=True)
	altura = Column(String, nullable=True)
	pais_nacimiento = Column(String, nullable=True)
	ciudad_nacimiento = Column(String, nullable=True)
	antiguedad_residencia = Column(String, nullable=True)
	deportes_practica = Column(String, nullable=False)


	def  __init__(self, email, nombre, apellido,tipo_id,numero_identificacion,genero,fecha_nacimiento,peso, altura,pais_nacimiento,ciudad_nacimiento,antiguedad_residencia,deportes_practica):
		self.email  = email
		self.nombre  = nombre
		self.apellido = apellido
		self.tipo_id = tipo_id
		self.numero_identificacion = numero_identificacion
		self.genero = genero
		self.fecha_nacimiento = fecha_nacimiento
		self.peso = peso
		self.altura = altura
		self.pais_nacimiento = pais_nacimiento
		self.ciudad_nacimiento = ciudad_nacimiento
		self.antiguedad_residencia = antiguedad_residencia
		self.deportes_practica = deportes_practica


class UsuarioJsonSchema(Schema):
	id = fields.UUID(dump_only=True)
	email  = fields.Str()
	nombre  = fields.Str()
	apellido = fields.Str()
	tipo_id = fields.Str()
	numero_identificacion = fields.Str()
	genero = fields.Str()
	fecha_nacimiento = fields.Str()
	peso = fields.Str()
	altura = fields.Str()
	pais_nacimiento = fields.Str()
	ciudad_nacimiento = fields.Str()
	antiguedad_residencia = fields.Str()
	deportes_practica = fields.Str()


