from sqlite3 import Date
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy  import  Column, ForeignKey, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Reunion(Base):
	__tablename__  =  'reunion'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	fecha = Column(db.DateTime(), nullable=False)
	lugar = Column(String, nullable=False)
	id_entrenador = Column(UUID(as_uuid=True), ForeignKey("entrenador.id"),primary_key=True, nullable=False)
	id_usuario = Column(UUID(as_uuid=True), nullable=True)
		# Relationships
	entrenador = relationship("Entrenador")
    
	def  __init__(self, fecha, lugar, entrenador, usuario):
		self.fecha  = fecha
		self.lugar  = lugar
		self.id_entrenador  = entrenador
		self.id_usuario  = usuario
		
class ReunionJsonSchema(Schema):

	id = fields.UUID(dump_only=True)
	fecha  = fields.DateTime()
	lugar  = fields.Str()
	id_entrenador  = fields.Str()
	id_usuario  = fields.Str()

class ReunionDisponobleJsonSchema(Schema):

	id = fields.UUID(dump_only=True)
	fecha  = fields.Str()
	lugar  = fields.Str()
	id_entrenador  = fields.Str()
	id_usuario  = fields.Str()
	nombre_entrenador = fields.Str()
	detalle_entrenador = fields.Str()


