import pytest
import random
from unittest.mock import patch
from faker import Faker
from unittest.mock import patch
from src.comandos.obtener_socios import ObtenerSocios
from src.modelos.socio import Socio
from test.mock_session import MockSession

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN =  fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_socios(mock_session, requests_mock):
    socio_mock = socios_mock()
    mock_session_instance = mock_session.return_value

    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = socio_mock

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
 
    service = ObtenerSocios(session=mock_session_instance, headers={"Authorization": "Bearer a"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def socios_mock():
    return [Socio(fake.safe_email(), fake.name(), fake.last_name(), random.choice(['CC', 'TI', 'CE', 'PAS']), fake.pyint(min_value=1000), fake.user_name(), fake.password(), fake.uuid4())]


