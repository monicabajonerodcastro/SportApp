import datetime
import pytest
from unittest.mock import patch
from faker import Faker

from src.modelos.reunion import Reunion
from src.comandos.asignar_reunion_usuario import AsignarReunionUsuario
from test.mock_session import MockSession

fake = Faker()
_ID_USUARIO = fake.uuid4()
_ID = fake.uuid4()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_asignar_reunion_usuario(mock_session, requests_mock):
    mock_reunion = reunion_mock_disponibles()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_reunion

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": fake.uuid4()})

    service = AsignarReunionUsuario(session=mock_session_instance, id=_ID,
                                    headers={"Authorization": "Bearer"})
    result = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0
    
def reunion_mock_disponibles():
    return [Reunion(datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), fake.name(), fake.uuid4(),None)]
