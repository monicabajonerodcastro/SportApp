import datetime
import pytest
import random
from unittest.mock import patch
from faker import Faker
from unittest.mock import patch
from src.comandos.obtener_reuniones import ObtenerReuniones, ObteneReunionesDisponibles
from src.modelos.reunion import Reunion
from test.mock_session import MockSession

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN =  fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


@patch('test.mock_session', autospec=True)
def test_obtener_reuniones(mock_session, requests_mock):
    reunion_mock = reunion_mock_all()
    mock_session_instance = mock_session.return_value

    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = reunion_mock

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
 
    service = ObtenerReuniones(session=mock_session_instance, headers={"Authorization": "Bearer"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def reunion_mock_all():
    return [Reunion(datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), fake.name(), fake.uuid4(), fake.uuid4())]


@patch('test.mock_session', autospec=True)
def test_obtener_reuniones_disponibles(mock_session, requests_mock):
    reunion_mock = reunion_mock_disponibles()
    mock_session_instance = mock_session.return_value

    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = reunion_mock

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
 
    service = ObteneReunionesDisponibles(session=mock_session_instance, headers={"Authorization": "Bearer"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def reunion_mock_disponibles():
    return [Reunion(datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), fake.name(), fake.uuid4(),None)]

