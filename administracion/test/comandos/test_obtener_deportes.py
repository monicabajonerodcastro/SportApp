import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_deportes import ObtenerDeportes
from src.modelos.deporte import Deporte
from test.mock_session import MockSession

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_deportes(mock_session):
    mock_deporte = deportes_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = mock_deporte
    
    service = ObtenerDeportes(session=mock_session_instance)
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def deportes_mock():
    return [Deporte(nombre=fake.text())]


