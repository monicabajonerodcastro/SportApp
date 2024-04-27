import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_planes_entrenamiento import ObtenerPlanesEntrenamiento
from src.modelos.plan_entrenamiento import PlanEntrenamiento
from test.mock_session import MockSession

fake = Faker()
_TOKEN =  fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_planes_entrenamiento(mock_session, requests_mock):
    plan_mock = plan_mockq()
    mock_session_instance = mock_session.return_value

    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = plan_mock

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
 
    service = ObtenerPlanesEntrenamiento(session=mock_session_instance, headers={"Authorization": "Bearer"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def plan_mockq():
    return [PlanEntrenamiento(nombre=fake.text(), deporte=fake.uuid4())]
