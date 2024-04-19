import datetime
import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from test.mock_session import MockSession

from src.comandos.crear_reunion import CrearReunion
from src.modelos.reunion import Reunion
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField,InvalidFormatField
import random, os

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_reunion(session, reunion_mock, headers):
    return CrearReunion(session,headers,
                        {"fecha": reunion_mock.fecha,
                        "lugar": reunion_mock.lugar,
                        "id_entrenador": reunion_mock.id_entrenador,
                        "id_usuario": reunion_mock.id_usuario
                        }                       
                     )


def reunion_mock():
    return Reunion(datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), fake.name(), fake.uuid4(), fake.uuid4())


@patch('test.mock_session', autospec=True)
def test_crear_reunion(mock_session,requests_mock):
    my_reunion_mock = reunion_mock()

    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_reunion_mock
    session.query.return_value = query

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    crearReunion = crear_reunion(session, my_reunion_mock, headers={"Authorization": "Bearer"})
    result = crearReunion.execute()
    assert result == "Reunión registrada con éxito"

@patch('test.mock_session', autospec=True)
def test_crear_reunion_missing_requiredfield(mock_session,requests_mock):
    my_reunion_mock = reunion_mock()
    my_reunion_mock.id_entrenador=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_reunion_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_reunion(session, my_reunion_mock,""),
        service.execute()
        
    assert exc_info.value.code == 404


