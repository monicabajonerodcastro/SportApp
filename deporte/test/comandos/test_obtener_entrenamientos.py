import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.obtener_entrenamientos import ObtenerEntrenamientos
from src.modelos.entrenamiento import Entrenamiento
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
    mock_entrenamiento = entrenamientos_mock()

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.all.return_value = mock_entrenamiento
    service = ObtenerEntrenamientos(session=mock_session_instance, headers={"Authorization": "Bearer"})
    (result, _) = service.execute()

    assert mock_session_instance.query.called
    assert len(result) > 0


def entrenamientos_mock():
    return [Entrenamiento(fake.name(), fake.date_this_decade(), fake.date_this_decade(), fake.name(),
                          random.choice(['DIARIO', 'SEMANAL', 'POR_DIAS']), fake.sentences(),
                          random.choice(['Atletismo', 'Ciclismo']))]
