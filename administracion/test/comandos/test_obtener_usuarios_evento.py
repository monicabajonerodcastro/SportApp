import datetime
import random
import pytest
from unittest.mock import patch
from faker import Faker

from src.modelos.evento import Evento
from src.modelos.evento_usuario_u import EventoUsuarioU
from src.comandos.obtener_usuarios_evento import ObtenerUsuariosEvento
from test.mock_session import MockSession
from src.errores.errores import InvalidAuthenticationError

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN = fake.uuid4()
_ID_EVENTO = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_usuarios_evento(mock_session, requests_mock, mocker):
    evento_usuario_mock = evento_usuario_mockq()
    evento_mock=evento_mockq()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = evento_mock
    mock_query.filter.return_value.first.return_value = evento_usuario_mock

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
  
    service = ObtenerUsuariosEvento(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_evento=evento_usuario_mock.id_evento)
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

@patch('test.mock_session', autospec=True)
def test_entrenamientos_plan_id_sin_autorizacion(mock_session, mocker):
    evento_usuario_mock = evento_usuario_mockq()
    evento_mock=evento_mockq()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = evento_mock
    mock_query.filter.return_value.first.return_value = evento_usuario_mock

    with pytest.raises(InvalidAuthenticationError):
        ObtenerUsuariosEvento(session=mock_session_instance, headers={}, id_evento=evento_usuario_mock.id_evento).execute()

def evento_usuario_mockq():
    return EventoUsuarioU(id_usuario=fake.uuid4(), id_evento=_ID_EVENTO)

def evento_mockq():
    return Evento(_ID_EVENTO, fake.name(), datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), 
                  fake.uuid4(), fake.uuid4(), fake.name())