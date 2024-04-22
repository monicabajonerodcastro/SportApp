import pytest
from unittest.mock import MagicMock
from faker import Faker

from src.commands.crear_perfil_deportivo import CrearPerfilDeportivo
from src.models.perfil_deportivo import PerfilDeportivo
from src.models.usuario import Usuario
from test.mock_session import MockSession
from src.errors.errors import MissingRequiredField,InvalidUser,PerfilDeportivoAlreadyRegistered
import random

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_perfil_deportivo(session, perfildeportivo_mock):
    return CrearPerfilDeportivo(session,
                        {
                            "id_usuario" : perfildeportivo_mock.id_usuario, 
                            "genero" :perfildeportivo_mock.genero ,  
                            "edad" : perfildeportivo_mock.edad , 
                            "peso" : perfildeportivo_mock.peso ,  
                            "altura" : perfildeportivo_mock.altura , 
                            "pais_nacimiento" :perfildeportivo_mock.pais_nacimiento , 
                            "ciudad_nacimiento" : perfildeportivo_mock.ciudad_nacimiento ,
                            "pais_residencia" :perfildeportivo_mock.pais_residencia , 
                            "ciudad_residencia" :perfildeportivo_mock.ciudad_residencia , 
                            "antiguedad_residencia" :perfildeportivo_mock.antiguedad_residencia , 
                            "imc" : perfildeportivo_mock.imc , 
                            "horas_semanal" : perfildeportivo_mock.horas_semanal ,
                            "peso_objetivo" :perfildeportivo_mock.peso_objetivo,
                            "tipo_sangre": perfildeportivo_mock.tipo_sangre,
                            "deporte": perfildeportivo_mock.deporte,
                            "direccion": perfildeportivo_mock.direccion
  }
                     )


def perfildeportivo_mock():
    return PerfilDeportivo( fake.uuid4(),random.choice(['F', 'M', 'O']), fake.pyint(min_value=15), fake.pyint(), fake.pyint(max_value=250), fake.country(), fake.city(),fake.country(), fake.city(),fake.pyint(),fake.pyfloat(max_value=100,right_digits=2),fake.pyint(),fake.pyfloat(right_digits=2),"","","","","","",fake.name(),fake.name(), fake.word())

def usuario_mock():
    return Usuario(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4(), "DEPORTISTA")

def test_crear_perfildeportivo_missing_requiredfield():
    my_perfildeportivo_mock= perfildeportivo_mock()
    my_perfildeportivo_mock.id_usuario=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = usuario_mock()
    session.query.return_value = query


    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_perfil_deportivo(session, my_perfildeportivo_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "No se encontró el usuario en la petición"


def test_crear_perfildeportivo_usuario_no_registrado():
    my_perfildeportivo_mock= perfildeportivo_mock()
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = None
    session.query.return_value = query


    with pytest.raises(InvalidUser) as exc_info:
        service = crear_perfil_deportivo(session, my_perfildeportivo_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "Usuario no existe"

def test_crear_perfildeportivo_perfil_ya_registrado():
    my_perfildeportivo_mock= perfildeportivo_mock()
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = usuario_mock()
    session.query.return_value = query


    with pytest.raises(PerfilDeportivoAlreadyRegistered) as exc_info:
        service = crear_perfil_deportivo(session, my_perfildeportivo_mock)
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "Perfil Deportivo ya existe"






