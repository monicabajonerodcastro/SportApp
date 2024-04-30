import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_paises import ObtenerPaises
from src.modelos.pais import Pais
from test.mock_session import MockSession

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_paises(mock_session):
    mock_pais = paises_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = mock_pais
    
    service = ObtenerPaises(session=mock_session_instance)
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def paises_mock():
    return [Pais(codigo=fake.text(), nombre=fake.text())]


