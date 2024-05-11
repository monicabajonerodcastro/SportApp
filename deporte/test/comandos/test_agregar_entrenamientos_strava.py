import pytest
from unittest.mock import patch
from faker import Faker

from src.comandos.agregar_entrenamientos_strava import AgregarEntrenamientosStrava
from src.modelos.entrenamiento import Entrenamiento
from test.mock_session import MockSession
import random

fake = Faker()


@pytest.fixture
def mock_session():
    return MockSession()

@patch('src.servicios.http.requests.post')
@patch('test.mock_session', autospec=True)
def test_agregar_entrenamientos_strava(mock_session, requests_mock):
    requests_mock.return_value.status_code = 201
   
    mock_session_instance = mock_session.return_value

    service = AgregarEntrenamientosStrava(session=mock_session_instance, headers={"Authorization": "Bearer"}, activities=activities_mock())
    (result, _) = service.execute()

    assert len(result) > 0


def activities_mock():
    activities=[{
            "name": fake.name(),
            "start_date" : fake.date(),
            "location_country" :  fake.name(),
            "distance" :  fake.pyint(),
            "type" :  fake.name()

    },{
            "name": fake.name(),
            "start_date" : fake.date(),
            "location_country" :  fake.name(),
            "distance" :  fake.pyint(),
            "type" :  fake.name()

    }]

    return activities