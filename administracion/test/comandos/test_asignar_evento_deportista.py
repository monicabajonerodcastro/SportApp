import pytest
from unittest.mock import patch
from faker import Faker
import datetime

from src.modelos.evento import Evento
from src.comandos.asignar_evento_deportista import AsignarEventoDeportista
from src.errores.errores import BadRequestError, InvalidAuthenticationError
from test.mock_session import MockSession

fake = Faker()
_ID_USUARIO = fake.uuid4()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_asignar_evento_deportista(mock_session, requests_mock):

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    (result, status_code) = AsignarEventoDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "}, 
                                                      evento=mock_evento()).execute()
    assert mock_session_instance.query.called
    assert result.get("respuesta")
    assert status_code == 200
    assert len(result["respuesta"]) > 0


@patch('test.mock_session', autospec=True)
def test_asignar_evento_deportista_sin_autorizacion(mock_session):

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = None

    with pytest.raises(InvalidAuthenticationError):
         AsignarEventoDeportista(session=mock_session_instance, headers={}, 
                                                      evento=mock_evento()).execute()
    
    assert not mock_session_instance.query.called


@patch('test.mock_session', autospec=True)
def test_asignar_evento_deportista_ya_creado(mock_session, requests_mock):
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_evento()

    with pytest.raises(BadRequestError):
          AsignarEventoDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "}, 
                                                      evento=mock_evento()).execute()
    

def mock_evento():
    evento = Evento(fake.uuid4(),fake.name(),datetime.datetime.strptime(fake.date(),'%Y-%m-%d'),datetime.datetime.strptime(fake.date(),'%Y-%m-%d'),fake.uuid4(), fake.uuid4(),fake.name()),
    return evento


