from marshmallow import Schema, fields
from sqlalchemy  import  Column, String,Integer,Float,ForeignKey
from src.models.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class PerfilDeportivo(Base):
	__tablename__  =  'perfil_deportivo'
	id = Column(UUID(as_uuid=True),  default=uuid.uuid4)
	genero = Column(String, nullable=False)
	edad = Column(Integer, nullable=False)
	peso = Column(String, nullable=False)
	altura = Column(Integer, nullable=False)
	pais_nacimiento = Column(String, nullable=False)
	ciudad_nacimiento = Column(String, nullable=True)
	pais_residencia = Column(String, nullable=False)
	ciudad_residencia = Column(String, nullable=False)
	antiguedad_residencia =Column(Integer, nullable=False)
	imc = Column(Float, nullable=True)
	horas_semanal = Column(Integer, nullable=True)
	peso_objetivo = Column(Float, nullable=True)
	alergias = Column(String, nullable=True)
	preferencia_alimenticia = Column(String, nullable=True)
	plan_nutricional = Column(String, nullable=True)
	url_historia_clinica = Column(String, nullable=True)
	vo2max = Column(Float, nullable=True,default=0.0)
	ftp = Column(Integer, nullable=True,default=0)
	id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"),primary_key=True)
	deporte = Column(String, nullable=True)
	tipo_sangre = Column(String, nullable=True)
	
	# Relationships
	usuario = relationship("Usuario")

	def  __init__(self, id_usuario,genero, edad, peso,altura,pais_nacimiento,ciudad_nacimiento,pais_residencia,ciudad_residencia,antiguedad_residencia,
			   imc,horas_semanal,peso_objetivo,alergias,preferencia_alimenticia,plan_nutricional,url_historia_clinica,vo2max,ftp,deporte,tipo_sangre):
			self.id_usuario = id_usuario
			self.genero = genero
			self.edad = edad
			self.peso = peso
			self.altura = altura
			self.pais_nacimiento = pais_nacimiento
			self.ciudad_nacimiento = ciudad_nacimiento
			self.pais_residencia = pais_residencia
			self.ciudad_residencia = ciudad_residencia
			self.antiguedad_residencia = antiguedad_residencia
			self.imc = imc
			self.horas_semanal = horas_semanal
			self.peso_objetivo = peso_objetivo
			self.alergias = alergias
			self.preferencia_alimenticia = preferencia_alimenticia
			self.plan_nutricional = plan_nutricional
			self.url_historia_clinica = url_historia_clinica
			self.vo2max = vo2max
			self.ftp = ftp
			self.deporte = deporte
			self.tipo_sangre = tipo_sangre
		


class PerfilDeportivoJsonSchema(Schema):
	id = fields.UUID(dump_only=True)
	id_usuario = fields.Str()
	genero = fields.Str()
	edad = fields.Str()
	peso = fields.Str()
	altura = fields.Str()
	pais_nacimiento = fields.Str()
	ciudad_nacimiento = fields.Str()
	pais_residencia = fields.Str()
	ciudad_residencia = fields.Str()
	antiguedad_residencia = fields.Str()
	imc = fields.Str()
	horas_semanal = fields.Str()
	peso_objetivo = fields.Str()
	alergias = fields.Str()
	preferencia_alimenticia = fields.Str()
	plan_nutricional = fields.Str()
	url_historia_clinica = fields.Str()
	vo2max = fields.Str()
	ftp = fields.Str()
	deporte = fields.Str()
	tipo_sangre = fields.Str()


