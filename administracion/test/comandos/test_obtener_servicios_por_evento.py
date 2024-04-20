import pytest
from unittest.mock import patch
from faker import Faker

from src.errores.errores import InvalidAuthenticationError
from src.comandos.obtener_servicios_por_evento import ObtenerServiciosPorEvento
from src.modelos.evento_servicio import EventoServicio
from src.modelos.producto_servicio import ProductoServicio
from src.modelos.evento import Evento
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
def test_obtener_servicios_por_evento(mock_session, requests_mock, mocker):
    evento_servicio_mock = mock_eventos_servicios()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.all.return_value = evento_servicio_mock

    producto_servicio_mock = mock_producto_servicio()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = producto_servicio_mock

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    service = ObtenerServiciosPorEvento(session=mock_session_instance, headers={"Authorization": "Bearer "}, evento=mock_evento().__dict__)
    (result, _) = service.execute()
    assert mock_session_instance.query.called
   
@patch('test.mock_session', autospec=True)
def test_obtener_evento_id_sin_autorizacion(mock_session, mocker):
    evento_servicio_mock = mock_eventos_servicios()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.all.return_value = evento_servicio_mock

    with pytest.raises(InvalidAuthenticationError):
        ObtenerServiciosPorEvento(session=mock_session_instance, headers={}, evento=mock_evento().__dict__).execute()
    
    assert not mock_session_instance.query.called


def mock_eventos_servicios():
    return [EventoServicio(id_evento=_ID_EVENTO, id_servicio=_ID_SERVICIO)]

def mock_producto_servicio():
    return ProductoServicio(fake.name(),fake.pyint(min_value=1000), fake.name(), fake.name(), fake.uuid4(),fake.uuid4())

def mock_evento():
    return Evento(id=fake.uuid4(), nombre=fake.name(), fecha_inicio=fake.date_time(), fecha_fin=fake.date_time(), id_deporte=_ID_DEPORTE, id_socio=_ID_SOCIO, detalle=fake.text())



