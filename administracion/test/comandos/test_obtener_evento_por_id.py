import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_evento_por_id import ObtenerEventoId
from src.modelos.evento import Evento
from test.mock_session import MockSession
from src.errores.errores import InvalidAuthenticationError

fake = Faker()
_SECRET_TEST = "secret"
_ID_DEPORTE = fake.uuid4()
_ID_SOCIO = fake.uuid4()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_evento_id(mock_session, requests_mock, mocker):
    mock_evento = evento_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_evento

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    service = ObtenerEventoId(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_evento=mock_evento.id)
    (result, _) = service.execute()
    assert mock_session_instance.query.called
    assert result["respuesta"]["nombre"] == mock_evento.nombre

@patch('test.mock_session', autospec=True)
def test_obtener_evento_id_sin_autorizacion(mock_session, mocker):
    mock_evento = evento_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_evento

    with pytest.raises(InvalidAuthenticationError):
        ObtenerEventoId(session=mock_session_instance, headers={}, id_evento=mock_evento.id).execute()
    
    assert not mock_session_instance.query.called

def evento_mock():
    return Evento(id=fake.uuid4(), nombre=fake.name(), fecha_inicio=fake.date_time(), fecha_fin=fake.date_time(), id_deporte=_ID_DEPORTE, id_socio=_ID_SOCIO, detalle=fake.text())



