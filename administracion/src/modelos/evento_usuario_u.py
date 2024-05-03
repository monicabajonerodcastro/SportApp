import uuid
from marshmallow import Schema, fields
from sqlalchemy import Column, String
from src.modelos.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy  import  Column, ForeignKey

class EventoUsuarioU(Base):
	__tablename__  =  'evento_usuario_u'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	id_usuario = Column(UUID(as_uuid=True), nullable=False)
	id_evento = Column(UUID(as_uuid=True), ForeignKey("evento.id"), primary_key=True, nullable=False)
		# Relationships
	evento = relationship("Evento")

	def __init__(self, id_usuario, id_evento):
		self.id = uuid.uuid4()
		self.id_usuario = id_usuario
		self.id_evento = id_evento

class EventoUsuarioUSchema(Schema):
	id = fields.UUID(dump_only=True)
	id_usuario  = fields.Str()
	id_evento  = fields.Str()


    