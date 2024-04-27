import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.remover_plan_deportista import RemoverPlanDeportista
from src.comandos.asignar_plan_deportista import AsignarPlanDeportista
from test.mock_session import MockSession

fake = Faker()
_TOKEN = fake.uuid4()
_ID_PLAN = fake.uuid4()
_ID_USUARIO = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_remover_plan_deportista(mock_session, requests_mock):

    mock_session_instance = mock_session.return_value

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    (result, status_code) = RemoverPlanDeportista(session=mock_session_instance, headers={"Authorization": "Bearer "}, id_plan=_ID_PLAN).execute()

    assert status_code == 200
    assert result.get("respuesta")
    assert result.get("token")
    assert result["respuesta"] == "Plan desasigado exitosamente"
    assert result["token"] == _TOKEN
