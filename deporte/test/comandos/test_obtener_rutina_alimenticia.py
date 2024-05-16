import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_rutina_alimenticia import ObtenerRutinaAlimenticia
from src.modelos.rutina_alimenticia import RutinaAlimenticia
from test.mock_session import MockSession
import random

fake = Faker()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('src.servicios.http.requests.post')
@patch('test.mock_session', autospec=True)
def test_obtener_entrenamientos(mock_session, requests_mock):
    requests_mock.return_value.status_code = 200
    mock_session_instance = mock_session.return_value
    service = ObtenerRutinaAlimenticia(session=mock_session_instance, headers={"Authorization": "Bearer"}, json_request={"potencia": 100, "min_ritmo": 100, "max_ritmo": 120})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0


