import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from test.mock_session import MockSession

from src.comandos.crear_entrenador import CrearEntrenador
from src.modelos.entrenador import Entrenador
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField,InvalidFormatField
import random, os

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_entrenador(session, entrenador_mock, headers):
    return CrearEntrenador(session,headers,
                        {"email": entrenador_mock.email,
                        "nombre": entrenador_mock.nombre,
                        "apellido": entrenador_mock.apellido,
                        "tipo_identificacion": entrenador_mock.tipo_id,
                        "numero_identificacion": entrenador_mock.numero_identificacion,
                        "username": entrenador_mock.username,
                        "password": entrenador_mock.password,
                        "detalle": entrenador_mock.detalle,
                        "deporte": entrenador_mock.deporte,
                        }                     
                     )

def entrenador_mock():
    return Entrenador(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4(), fake.uuid4())

@patch('test.mock_session', autospec=True)
def test_crear_entrenador(mock_session,requests_mock):
    my_entrenador_mock = entrenador_mock()

    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_entrenador_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    crearEntrenador = crear_entrenador(session, my_entrenador_mock, headers={"Authorization": "Bearer"})
    result = crearEntrenador.execute()
    assert result == "Entrenador registrado con éxito"

@patch('test.mock_session', autospec=True)
def test_crear_entrenador_missing_requiredfield(mock_session,requests_mock):
    my_entrenador_mock = entrenador_mock()
    my_entrenador_mock.nombre=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_entrenador_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_entrenador(session, my_entrenador_mock,""),
        service.execute()
        
    assert exc_info.value.code == 404


@patch('test.mock_session', autospec=True)
def test_crear_entrenador_invalid_formatfield(mock_session,requests_mock):
    my_entrenador_mock = entrenador_mock()
    my_entrenador_mock.email="uno@uno."
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_entrenador_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})


    with pytest.raises(InvalidFormatField) as exc_info:
        service = crear_entrenador(session, my_entrenador_mock,"")
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "Parámeto(s) con formato inválido"

