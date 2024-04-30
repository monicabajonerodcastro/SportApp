import random
import pytest
from unittest.mock import patch
from faker import Faker

from src.modelos.entrenamiento import Entrenamiento
from src.modelos.plan_entrenamiento_u import PlanEntrenamientoU
from src.comandos.obtener_entrenamientos_plan import ObtenerEntrenamientosPlan
from test.mock_session import MockSession
from src.errores.errores import InvalidAuthenticationError

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_entrenamientos_plan_id(mock_session, requests_mock, mocker):
    plan_entrenamiento_mock = plan_entrenamiento_mockq()
    entrenamiento_mock=entrenamiento_mockq()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = entrenamiento_mock
    mock_query.filter.return_value.first.return_value = plan_entrenamiento_mock

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
  
    service = ObtenerEntrenamientosPlan(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_plan=plan_entrenamiento_mock.id_plan)
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0

@patch('test.mock_session', autospec=True)
def test_entrenamientos_plan_id_sin_autorizacion(mock_session, mocker):
    plan_entrenamiento_mock = plan_entrenamiento_mockq()
    entrenamiento_mock=entrenamiento_mockq()

    mocker.patch("src.servicios.secret.get_secret", return_value=_SECRET_TEST)

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.first.return_value = entrenamiento_mock
    mock_query.filter.return_value.first.return_value = plan_entrenamiento_mock

    with pytest.raises(InvalidAuthenticationError):
        ObtenerEntrenamientosPlan(session=mock_session_instance, headers={}, id_plan=plan_entrenamiento_mock.id_plan).execute()

def plan_entrenamiento_mockq():
    return PlanEntrenamientoU(id_plan=fake.uuid4(), id_entrenamiento=fake.uuid4())

def entrenamiento_mockq():
    return Entrenamiento(fake.name(), fake.date_this_decade(), fake.date_this_decade(), fake.name(),
                         random.choice(['DIARIO', 'SEMANAL', 'POR_DIAS']), fake.sentences(),
                         random.choice(['Atletismo', 'Ciclismo']))