import pytest
from unittest.mock import patch
from faker import Faker
import datetime

from src.comandos.eliminar_evento_deportista import EliminarEventoDeportista
from src.modelos.evento import Evento
from src.comandos.asignar_evento_deportista import AsignarEventoDeportista
from src.errores.errores import InvalidAuthenticationError, NotFoundError
from test.mock_session import MockSession

fake = Faker()
_ID_USUARIO = fake.uuid4()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_eliminar_evento_deportista(mock_session, requests_mock):

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_evento()

    (result, status_code) = EliminarEventoDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "}, 
                                                      id_evento=fake.uuid4()).execute()
    assert mock_session_instance.query.called
    assert result.get("respuesta")
    assert status_code == 200


@patch('test.mock_session', autospec=True)
def test_eliminar_evento_deportista_sin_autorizacion(mock_session):

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    with pytest.raises(InvalidAuthenticationError):
         EliminarEventoDeportista(session=mock_session_instance, headers={}, 
                                                      id_evento=fake.uuid4()).execute()
    
    assert not mock_session_instance.query.called


@patch('test.mock_session', autospec=True)
def test_eliminar_evento_deportista_no_existe(mock_session, requests_mock):
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    with pytest.raises(NotFoundError):
          EliminarEventoDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "}, 
                                                      id_evento=fake.uuid4()).execute()
    

def mock_evento():
    evento = Evento(fake.uuid4(),fake.name(),datetime.datetime.strptime(fake.date(),'%Y-%m-%d'),datetime.datetime.strptime(fake.date(),'%Y-%m-%d'),fake.uuid4(), fake.uuid4(),fake.name())
    return evento


