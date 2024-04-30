import pytest
import random
from unittest.mock import patch
from faker import Faker
from unittest.mock import patch
from src.comandos.obtener_producto_servicios import ObtenerProductoServicios
from src.modelos.producto_servicio import ProductoServicio
from test.mock_session import MockSession

fake = Faker()

_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_producto_servicio(mock_session,requests_mock):
    my_producto_servicio_mock = producto_servicio_mock()
    mock_session_instance = mock_session.return_value

    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = my_producto_servicio_mock
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    service = ObtenerProductoServicios(session=mock_session_instance,headers={"Authorization": "Bearer"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0



def producto_servicio_mock():
    return [ProductoServicio(fake.name(),fake.pyint(min_value=1000), fake.name(), fake.name(), fake.uuid4(),fake.uuid4())]
