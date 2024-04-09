import pytest
import random
from unittest.mock import patch
from faker import Faker
from unittest.mock import patch, MagicMock
from src.comandos.obtener_socios import ObtenerSocios
from src.modelos.socio import Socio
from src.errores.errores import InvalidAuthenticationError
from test.mock_session import MockSession

fake = Faker()
_SECRET_TEST = "secret"

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_socios(mock_session):
    socio_mock = socios_mock()
    mock_session_instance = mock_session.return_value

    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = socio_mock
 
    service = ObtenerSocios(session=mock_session_instance, headers={"Authorization": "Bearer a"}, test=True)
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def socios_mock():
    return [Socio(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4())]


