from src.models.perfil_deportivo import PerfilDeportivo
from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredField,InvalidUser,PerfilDeportivoAlreadyRegistered
from src.models.usuario import Usuario


class CrearPerfilDeportivo(BaseCommannd):
    def __init__(self, session, json_request) -> None:
        

        id_usuario = json_request["id_usuario"] if "id_usuario" in json_request.keys() else ""
        genero = json_request["genero"] if "genero" in json_request.keys() else ""
        edad = json_request["edad"] if "edad" in json_request.keys() else ""
        peso = json_request["peso"] if "peso" in json_request.keys() else ""
        altura = json_request["altura"] if "altura" in json_request.keys() else ""
        pais_nacimiento = json_request["pais_nacimiento"] if "pais_nacimiento" in json_request.keys() else ""
        ciudad_nacimiento = json_request["ciudad_nacimiento"] if "ciudad_nacimiento" in json_request.keys() else ""
        pais_residencia = json_request["pais_residencia"] if "pais_residencia" in json_request.keys() else ""
        ciudad_residencia = json_request["ciudad_residencia"] if "ciudad_residencia" in json_request.keys() else ""
        antiguedad_residencia = json_request["antiguedad_residencia"] if "antiguedad_residencia" in json_request.keys() else ""
        imc = json_request["imc"] if "imc" in json_request.keys() else ""
        horas_semanal = json_request["horas_semanal"] if "horas_semanal" in json_request.keys() else ""
        peso_objetivo = json_request["peso_objetivo"] if "peso_objetivo" in json_request.keys() else ""
        alergias = json_request["alergias"] if "alergias" in json_request.keys() else ""
        preferencia_alimenticia = json_request["preferencia_alimenticia"] if "preferencia_alimenticia" in json_request.keys() else ""
        plan_nutricional = json_request["plan_nutricional"] if "plan_nutricional" in json_request.keys() else ""
        url_historia_clinica = json_request["url_historia_clinica"] if "url_historia_clinica" in json_request.keys() else ""
        vo2max = json_request["vo2max"] if "vo2max" in json_request.keys() else "0.0"
        ftp = json_request["ftp"] if "ftp" in json_request.keys() else 0


        if (id_usuario =="" or genero =="" or  edad =="" or peso =="" or  altura =="" or pais_nacimiento =="" or ciudad_nacimiento =="" or
                pais_residencia =="" or ciudad_residencia =="" or antiguedad_residencia =="" or imc =="" or horas_semanal =="" or
                    peso_objetivo ==""  
                                ) :  
                                    raise MissingRequiredField()
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
                                ftp = ftp)
        
   
    def execute(self):
        self.session.add(self.perfil_deportivo)
        self.session.commit()
        return {"description" : "Perfil Deportivo Registrado con exito", "id": self.perfil_deportivo.id}
         
