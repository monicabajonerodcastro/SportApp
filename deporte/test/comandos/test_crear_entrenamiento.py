import pytest
from unittest.mock import patch, MagicMock
from faker import Faker

from src.comandos.crear_entrenamiento import CrearEntrenamiento
from src.modelos.entrenamiento import Entrenamiento
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField
import random

fake = Faker()
_SECRET_TEST = "secret"
_TOKEN = fake.uuid4()


@pytest.fixture
def mock_session():
    return MockSession()


def crear_entrenamiento(session, entrenamiento_mock, headers):
    return CrearEntrenamiento(session, headers,
                              {
                                  "nombre": entrenamiento_mock.nombre,
                                  "hora_inicio": entrenamiento_mock.hora_inicio,
                                  "hora_fin": entrenamiento_mock.hora_fin,
                                  "lugar": entrenamiento_mock.lugar,
                                  "frecuencia": entrenamiento_mock.frecuencia,
                                  "detalle": entrenamiento_mock.detalle,
                                  "deporte": entrenamiento_mock.deporte
                              }
                              )


def entrenamiento_mock():
    return Entrenamiento(fake.name(), fake.date_this_decade(), fake.date_this_decade(), fake.name(),
                         random.choice(['DIARIO', 'SEMANAL', 'POR_DIAS']), fake.sentences(),
                         random.choice(['Atletismo', 'Ciclismo']))

@patch('src.servicios.http.requests.post')
@patch('test.mock_session', autospec=True)
def test_crear_entrenamiento(mock_session, requests_mock):
    requests_mock.return_value.status_code = 200
    my_entrenamiento_mock = entrenamiento_mock()
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_entrenamiento_mock
    session.query.return_value = query
    crearEntrenamiento = crear_entrenamiento(session, my_entrenamiento_mock, headers={"Authorization": "Bearer"})
    result = crearEntrenamiento.execute()
    assert result == "Entrenamiento registrado con éxito"

@patch('src.comandos.crear_entrenamiento')
@patch('test.mock_session', autospec=True)
def test_crear_entrenamiento_missing_requiredfield(mock_session, requests_mock):
    my_entrenamiento_mock = entrenamiento_mock()
    my_entrenamiento_mock.nombre = ""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_entrenamiento_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})

    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_entrenamiento(session, my_entrenamiento_mock, ""),
        service.execute()

    assert exc_info.value.code == 404
