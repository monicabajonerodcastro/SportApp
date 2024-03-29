import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_planes import ObtenerPlan
from src.modelos.plan import Plan
from test.mock_session import MockSession

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_planes(mock_session):
    mock_plan = planes_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = mock_plan
    
    service = ObtenerPlan(session=mock_session_instance, headers={"Authorization": "Bearer"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

@patch('test.mock_session', autospec=True)
def test_obtener_planes_sin_autorizacion(mock_session):
    mock_plan = planes_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = mock_plan
    
    service = ObtenerPlan(session=mock_session_instance, headers={})
    (_, status) = service.execute()
    assert not mock_session_instance.query.called
    assert status == 403

def planes_mock():
    return [Plan(id=fake.uuid4(), nombre=fake.name(), funciones=fake.text(), valor_mensual=fake.pyint())]


