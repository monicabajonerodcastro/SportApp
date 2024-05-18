from src.modelos.rutina_alimenticia import RutinaAlimenticia
from src.modelos.producto_alimenticio import ProductoAlimenticio, ProductoAlimenticioSchema
from src.modelos.producto_rutina import ProductoRutina
from src.errores.errores import MissingRequiredField, NotFoundError, BadRequestError
from src.modelos.sesion_entrenamiento import EstadoSesionEntrenamiento, SesionEntrenamiento
from src.comandos.base_command import BaseCommand
from src.servicios import auth

_RUTINA_1 =  "Alta Potencia - Alto Ritmo"
_RUTINA_2 =  "Alta Potencia - Bajo Ritmo"
_RUTINA_3 =  "Baja Potencia - Alto Ritmo"
_RUTINA_4 =  "Baja Potencia - Bajo Ritmo"

producto_schema = ProductoAlimenticioSchema ()

def _validar_campo(campo, json, mensaje) -> None:
    if campo in json and json[campo] != "" and json[campo] != None:
        return json[campo]
    raise MissingRequiredField(description=mensaje)

def _validar_formato_numero(nombre, numero) -> None:
    try:
        float(numero)
    except Exception:
        raise BadRequestError(description="El campo ["+nombre+"] tiene un formato inválido" )

def _validar_rutina_existe(self, nombre) -> str:
    rutina = self.session.query(RutinaAlimenticia).filter(RutinaAlimenticia.nombre == nombre).first()
    if rutina is None:
        raise NotFoundError(description="En el momento no se encuentra una rutina alimenticia recomendada para los parámetros recibidos")
    else:
        productos = self.session.query(ProductoAlimenticio).join(ProductoRutina).filter(ProductoRutina.rutina_alimenticia == rutina.id).all()    
        return {"id": rutina.id, "nombre": rutina.nombre, "descripcion": rutina.descripcion, "productos": [producto_schema.dump(producto) for producto in productos]}  

class ObtenerRutinaAlimenticia(BaseCommand):
    def __init__(self, session, headers, json_request) -> None:
        self.session = session
        self.headers = headers

        self.potencia = _validar_campo("potencia", json_request, "No se encontró la potencia")
        self.min_ritmo = _validar_campo("min_ritmo", json_request, "No se encontró el ritmo cardiaco mínimo")
        self.max_ritmo = _validar_campo("max_ritmo", json_request, "No se encontró el ritmo cardiaco máximo")
        _validar_formato_numero("potencia", self.potencia)
        _validar_formato_numero("min_ritmo", self.min_ritmo)
        _validar_formato_numero("max_ritmo", self.max_ritmo)
        self.ritmo_promedio = (float(self.max_ritmo)+float(self.min_ritmo))/2
        self.potencia = float( self.potencia)

    def execute(self):
        nuevo_token = auth.validar_autenticacion(headers=self.headers)
        self.rutina=""
        if self.potencia>=200:
            if self.ritmo_promedio > 140:
                self.rutina=_validar_rutina_existe(self, _RUTINA_1)
            else:
                self.rutina=_validar_rutina_existe(self, _RUTINA_2)
        else:
            if self.ritmo_promedio > 140:
                self.rutina=_validar_rutina_existe(self, _RUTINA_3)
            else:
               self.rutina=_validar_rutina_existe(self, _RUTINA_4)

        return {"respuesta": self.rutina, "token": nuevo_token}, 200