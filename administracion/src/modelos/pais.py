from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.modelos.database import Base

class Pais(Base):
    __tablename__  =  'pais'
    codigo = Column(String, nullable=False, primary_key=True)
    nombre = Column(String, nullable=False)

    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

class PaisSchema(Schema):
	codigo  = fields.Str()
	nombre  = fields.Str()