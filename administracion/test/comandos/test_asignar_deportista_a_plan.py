import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.asignar_deportista_a_plan import AsignarDeportistaPlan
from src.modelos.plan import Plan
from src.errores.errores import InvalidAuthenticationError, MissingRequiredField
from test.mock_session import MockSession

fake = Faker()
_ID_PERSONA = fake.uuid4()
_ID_PLAN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_asignar_deportista(mock_session, requests_mock):
    mock_plan = plan_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_plan

    requests_mock.post('http://host-personas-test/personas/validar-token', json={})
    requests_mock.get(f'http://host-personas-test/personas/{_ID_PERSONA}', json={})

    service = AsignarDeportistaPlan(session=mock_session_instance, 
                                    headers={"Authorization": "Bearer"}, 
                                    json_request={"id_plan": _ID_PLAN, "id_deportista": _ID_PERSONA})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0


@patch('test.mock_session', autospec=True)
def test_asignar_deportista_sin_autorizacion(mock_session):
    mock_plan = plan_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_plan
    
    with pytest.raises(InvalidAuthenticationError):
        AsignarDeportistaPlan(session=mock_session_instance, headers={}, json_request={}).execute()

    assert not mock_session_instance.query.called


@patch('test.mock_session', autospec=True)
def test_asignar_deportista_sin_id_plan(mock_session, requests_mock):
    mock_plan = plan_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_plan

    requests_mock.post('http://host-personas-test/personas/validar-token', json={})
    
    with pytest.raises(MissingRequiredField):
        AsignarDeportistaPlan(session=mock_session_instance, headers={"Authorization": "Bearer"},  json_request={"id_deportista": _ID_PERSONA}).execute()

    assert not mock_session_instance.query.called

@patch('test.mock_session', autospec=True)
def test_asignar_deportista_sin_id_deportista(mock_session, requests_mock):
    mock_plan = plan_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = mock_plan

    requests_mock.post('http://host-personas-test/personas/validar-token', json={})
    
    with pytest.raises(MissingRequiredField):
        AsignarDeportistaPlan(session=mock_session_instance, headers={"Authorization": "Bearer"},  json_request={"id_plan": _ID_PLAN}).execute()

    assert not mock_session_instance.query.called

def plan_mock():
    return Plan(id=fake.uuid4(), nombre=fake.name(), llave=fake.text(), funciones=fake.text(), valor_mensual=fake.pyint())


