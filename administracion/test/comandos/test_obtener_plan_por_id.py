import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_plan_por_id import ObtenerPlanId
from src.modelos.plan import Plan
from test.mock_session import MockSession

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_plan_id(mock_session):
    plan_mock = plan_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = plan_mock
    
    service = ObtenerPlanId(mock_session_instance, plan_mock.email)
    result = service.execute()
    assert mock_session_instance.query.called
    assert result.name == plan_mock.name

def plan_mock():
    return Plan(id=fake.uuid4(), nombre=fake.name(), funciones=fake.text(), valor_mensual=fake.pyint())


