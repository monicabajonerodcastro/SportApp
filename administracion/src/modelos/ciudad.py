from marshmallow import Schema, fields
from sqlalchemy  import  Column, String
from src.modelos.database import Base

class Ciudad(Base):
    __tablename__  =  'ciudad'
    codigo = Column(String, nullable=False, primary_key=True)
    nombre = Column(String, nullable=False)
    pais = Column(String, nullable=False)

    def __init__(self, codigo, nombre, pais):
        self.codigo = codigo
        self.nombre = nombre
        self.pais = pais

class CiudadSchema(Schema):
	codigo  = fields.Str()
	nombre  = fields.Str()
	pais  = fields.Str()