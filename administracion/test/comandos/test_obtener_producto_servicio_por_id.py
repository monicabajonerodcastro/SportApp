import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_producto_servicio_por_id import ObtenerProductoServicioId
from test.mock_session import MockSession
from src.errores.errores import InvalidAuthenticationError
from src.modelos.producto_servicio import ProductoServicio


fake = Faker()
_SECRET_TEST = "secret"
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_producto_servicio_id(mock_session, requests_mock, mocker):
    mock_servicio = producto_servicio_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_servicio

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    service = ObtenerProductoServicioId(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_servicio=fake.uuid4())
    (result, _) = service.execute()
    assert mock_session_instance.query.called
    assert result["respuesta"]

@patch('test.mock_session', autospec=True)
def test_producto_servicio_id_sin_autorizacion(mock_session, mocker):
    mock_servicio = producto_servicio_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_servicio

    with pytest.raises(InvalidAuthenticationError):
       ObtenerProductoServicioId(session=mock_session_instance, headers={}, id_servicio=mock_servicio.id).execute()
    
    assert not mock_session_instance.query.called

def producto_servicio_mock():
    return ProductoServicio(fake.name(),fake.pyint(min_value=1000), fake.name(), fake.name(), fake.uuid4(),fake.uuid4())


