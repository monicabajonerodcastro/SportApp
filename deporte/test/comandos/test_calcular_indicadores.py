import datetime
import pytest
from unittest.mock import patch, MagicMock
from faker import Faker

from src.modelos.sesion_entrenamiento import SesionEntrenamiento, EstadoSesionEntrenamiento
from src.comandos.calcular_indicadores import CalcularIndicadores
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField
import random

fake = Faker()
_TOKEN = fake.uuid4()
_ID_USUARIO = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()

@patch('test.mock_session', autospec=True)
def test_calcular_indicadores_menos_8(mock_session, requests_mock):

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": _ID_USUARIO})

    mock_session_instance = mock_session.return_value
    mock_query = mock_session_instance.query.return_value
    mock_query.filter.return_value.order_by.return_value.all.return_value = mock_sesion_entrenamiento()

    (response, status_code) = CalcularIndicadores(session=mock_session_instance, headers={"Authorization" : "Bearer "}).execute()
    assert mock_session_instance.query.called
    assert response.get("respuesta")
    assert status_code == 200
    assert len(response.get("respuesta")) == 1

def mock_sesion_entrenamiento():
    sesion_entrenamiento = SesionEntrenamiento(_ID_USUARIO)
    sesion_entrenamiento.estado = EstadoSesionEntrenamiento.FINALIZADO.value
    sesion_entrenamiento.hora_inicio = datetime.datetime.now()
    hora_fin = datetime.timedelta(minutes=fake.pyint(min_value=7, max_value=30)) 
    sesion_entrenamiento.hora_fin = datetime.datetime.now() + hora_fin
    sesion_entrenamiento.min_ritmo = fake.pyint(min_value=80, max_value=90)
    sesion_entrenamiento.max_ritmo = fake.pyint(min_value=90, max_value=100)
    sesion_entrenamiento.potencia = fake.pyint(min_value=100, max_value=200)
    return [sesion_entrenamiento]