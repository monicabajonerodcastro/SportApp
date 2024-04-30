import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_plan_por_deportista import ObtenerPlanesDeportista
from src.modelos.plan_deportista import PlanDeportista
from test.mock_session import MockSession

fake = Faker()
_TOKEN =  fake.uuid4()
_ID_USUARIO =  fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_planes_deportista(mock_session, requests_mock):
    mock_plan_deportista = plan_deportista_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.all.return_value = mock_plan_deportista

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})
 
    service = ObtenerPlanesDeportista(session=mock_session_instance, headers={"Authorization": "Bearer"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

def plan_deportista_mock():
    return [PlanDeportista(id_deportista=fake.uuid4(), id_plan=fake.uuid4())]
