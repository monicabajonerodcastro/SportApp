import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from test.mock_session import MockSession

from src.comandos.crear_socio import CrearSocio
from src.modelos.socio import Socio
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField,InvalidFormatField
import random, os

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_socio(session, socio_mock, headers):
    return CrearSocio(session,headers,
                        {"email": socio_mock.email,
                        "nombre": socio_mock.nombre,
                        "apellido": socio_mock.apellido,
                        "tipo_identificacion": socio_mock.tipo_id,
                        "numero_identificacion": socio_mock.numero_identificacion,
                        "username": socio_mock.username,
                        "password": socio_mock.password,
                        "detalle": socio_mock.detalle}                   
                     )


def socio_mock():
    return Socio(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4())

@patch('test.mock_session', autospec=True)
def test_crear_socio(mock_session,requests_mock):
    my_socio_mock = socio_mock()

    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_socio_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    crearSocio = crear_socio(session, my_socio_mock, headers={"Authorization": "Bearer"})
    result = crearSocio.execute()
    assert result == "Socio Registrado con exito"

@patch('test.mock_session', autospec=True)
def test_crear_socio_missing_requiredfield(mock_session, requests_mock):
    my_socio_mock = socio_mock()
    my_socio_mock.nombre=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_socio_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    

    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_socio(session, my_socio_mock,""),
        service.execute()
        
    assert exc_info.value.code == 404

@patch('test.mock_session', autospec=True)
def test_crear_socio_invalid_formatfield(mock_session, requests_mock):
    my_socio_mock = socio_mock()
    my_socio_mock.email="uno@uno."
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_socio_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    

    with pytest.raises(InvalidFormatField) as exc_info:
        service = crear_socio(session, my_socio_mock,"")
        service.execute()


    assert exc_info.value.code == 400
    assert exc_info.value.description == "Parámeto(s) con formato inválido"




