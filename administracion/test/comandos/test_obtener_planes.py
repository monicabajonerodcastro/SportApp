import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_planes import ObtenerPlan
from src.modelos.plan import Plan
from src.errores.errores import InvalidAuthenticationError
from test.mock_session import MockSession

fake = Faker()
_SECRET_TEST = "secret"

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_obtener_planes(mock_session, requests_mock, mocker):
    mock_plan = planes_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = mock_plan

    requests_mock.post('http://host-personas-test/personas/validar-token', json={})
    
    service = ObtenerPlan(session=mock_session_instance, headers={"Authorization": "Bearer a"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

@patch('test.mock_session', autospec=True)
def test_obtener_planes_sin_autorizacion(mock_session, mocker):
    mock_plan = planes_mock()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = mock_plan
    
    with pytest.raises(InvalidAuthenticationError):
        ObtenerPlan(session=mock_session_instance, headers={}).execute()

    assert not mock_session_instance.query.called

def planes_mock():
    return [Plan(id=fake.uuid4(), nombre=fake.name(), llave=fake.text(), funciones=fake.text(), valor_mensual=fake.pyint())]


