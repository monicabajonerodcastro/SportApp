import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_ciudades import ObtenerCiudades
from src.modelos.ciudad import Ciudad
from test.mock_session import MockSession

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_ciudades(mock_session):
    mock_ciudad = ciudades_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.all.return_value = mock_ciudad
    
    service = ObtenerCiudades(session=mock_session_instance, id_pais=fake.text())
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def ciudades_mock():
    return [Ciudad(codigo=fake.text(), nombre=fake.text(), pais=fake.text())]


