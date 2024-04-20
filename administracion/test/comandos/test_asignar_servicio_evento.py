import pytest
from unittest.mock import patch
from faker import Faker

from src.errores.errores import InvalidAuthenticationError
from src.modelos.evento import Evento
from src.comandos.obtener_servicios_por_evento import ObtenerServiciosPorEvento
from src.modelos.evento_servicio import EventoServicio
from test.mock_session import MockSession

fake = Faker()
_ID_EVENTO = fake.uuid4()
_ID_DEPORTE = fake.uuid4()
_ID_SERVICIO = fake.uuid4()
_ID_SOCIO = fake.uuid4()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_asignar_servicio_evento(mock_session, requests_mock):
    mock_evento_servicio_list = mock_eventos_servicios()
    evento_mock = mock_evento()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.all.return_value = mock_evento_servicio_list

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    (result, status_code) = ObtenerServiciosPorEvento(session=mock_session_instance, headers={"Authorization": "Bearer "}, evento=evento_mock.__dict__).execute()
    assert mock_session_instance.query.called
    assert result.get("respuesta")
    assert status_code == 200
    assert len(result["respuesta"]) > 0

@patch('test.mock_session', autospec=True)
def test_asignar_servicio_evento_sin_autorizacion(mock_session):
    mock_evento_servicio_list = mock_eventos_servicios()
    evento_mock = mock_evento()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.all.return_value = mock_evento_servicio_list

    with pytest.raises(InvalidAuthenticationError):
        ObtenerServiciosPorEvento(session=mock_session_instance, headers={},  evento=evento_mock.__dict__).execute()
    
    assert not mock_session_instance.query.called

def mock_eventos_servicios():
    return [EventoServicio(id_evento=_ID_EVENTO, id_servicio=_ID_SERVICIO)]

def mock_evento():
    return Evento(id=fake.uuid4(), nombre=fake.name(), fecha_inicio=fake.date_time(), fecha_fin=fake.date_time(), id_deporte=_ID_DEPORTE, id_socio=_ID_SOCIO, detalle=fake.text())