from src.models.perfil_deportivo import PerfilDeportivo
from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredField,InvalidUser,PerfilDeportivoAlreadyRegistered
from src.models.usuario import Usuario


class CrearPerfilDeportivo(BaseCommannd):

    def _validar_campo(self, campo, json, mensaje) -> None:
        if campo in json and json[campo] != "" and json[campo] != None:
            return json[campo]
        raise MissingRequiredField(description=mensaje)
        
    def __init__(self, session, json_request) -> None:
        
        id_usuario = self._validar_campo("id_usuario", json_request, "No se encontró el usuario en la petición")
        genero = self._validar_campo("genero", json_request, "No se encontró el genero en la petición")
        edad = self._validar_campo("edad", json_request, "No se encontró la edad en la petición")
        peso = self._validar_campo("peso", json_request, "No se encontró el peso en la petición")
        altura = self._validar_campo("altura", json_request, "No se encontró la altura en la petición")
        pais_nacimiento = self._validar_campo("pais_nacimiento", json_request, "No se encontró el país de nacimiento en la petición")
        ciudad_nacimiento = self._validar_campo("ciudad_nacimiento", json_request, "No se encontró la ciudad de nacimiento en la petición")
        pais_residencia = self._validar_campo("pais_residencia", json_request, "No se encontró el pais de residencia en la petición")
        ciudad_residencia = self._validar_campo("ciudad_residencia", json_request, "No se encontró la ciudad de residencia en la petición")
        antiguedad_residencia = self._validar_campo("antiguedad_residencia", json_request, "No se encontró la antigueda de residencia en la petición")
        imc = self._validar_campo("imc", json_request, "No se encontró el imc en la petición")
        horas_semanal = self._validar_campo("horas_semanal", json_request, "No se encontró la cantidad de horas semanal en la petición")
        peso_objetivo = self._validar_campo("peso_objetivo", json_request, "No se encontró el peso objetivo en la petición")
        tipo_sangre = self._validar_campo("tipo_sangre", json_request, "No se encontró el tipo de sangre en la petición")
        deporte = self._validar_campo("deporte", json_request, "No se encontró el deporte en la petición")

        alergias = json_request["alergias"] if "alergias" in json_request.keys() else ""
        preferencia_alimenticia = json_request["preferencia_alimenticia"] if "preferencia_alimenticia" in json_request.keys() else ""
        plan_nutricional = json_request["plan_nutricional"] if "plan_nutricional" in json_request.keys() else ""
        url_historia_clinica = json_request["url_historia_clinica"] if "url_historia_clinica" in json_request.keys() else ""

        vo2max = json_request["vo2max"] if "vo2max" in json_request.keys() else "0.0"
        ftp = json_request["ftp"] if "ftp" in json_request.keys() else 0

        self.session = session
        usuario = self.session.query(Usuario).filter(Usuario.id == id_usuario).first()
        if usuario is None :
                raise InvalidUser()
     
        perfildeportivo = self.session.query(PerfilDeportivo).filter(PerfilDeportivo.id_usuario == id_usuario).first()
        if perfildeportivo is not None :
                raise PerfilDeportivoAlreadyRegistered()
        
        self.perfil_deportivo = PerfilDeportivo(
                                id_usuario=id_usuario,
                                genero = genero,
                                edad = edad,
                                peso = peso,
                                altura = altura,
                                pais_nacimiento = pais_nacimiento,
                                ciudad_nacimiento = ciudad_nacimiento,
                                pais_residencia = pais_residencia,
                                ciudad_residencia = ciudad_residencia,
                                antiguedad_residencia = antiguedad_residencia,
                                imc = imc,
                                horas_semanal = horas_semanal,
                                peso_objetivo = peso_objetivo,
                                alergias = alergias,
                                preferencia_alimenticia = preferencia_alimenticia,
                                plan_nutricional = plan_nutricional,
                                url_historia_clinica = url_historia_clinica,
                                vo2max = vo2max,
                                ftp = ftp,
                                tipo_sangre=tipo_sangre,
                                deporte=deporte)
   
    def execute(self):
        self.session.add(self.perfil_deportivo)
        self.session.commit()
        return {"description" : "Perfil Deportivo Registrado con exito", "id": self.perfil_deportivo.id}
         
