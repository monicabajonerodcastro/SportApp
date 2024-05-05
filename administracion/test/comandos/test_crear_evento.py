import datetime
import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from test.mock_session import MockSession

from src.comandos.crear_evento import CrearEvento
from src.modelos.evento import Evento
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField

fake = Faker()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_evento(session, evento_mock, headers):
    return CrearEvento(session,headers,
                        {"nombre": evento_mock.nombre,
                        "fecha_inicio": evento_mock.fecha_inicio,
                        "fecha_fin": evento_mock.fecha_fin,
                        "id_deporte": evento_mock.id_deporte,
                        "id_socio": evento_mock.id_socio,
                        "detalle": evento_mock.detalle,
                        "ubicacion": {
                            "id": fake.uuid4(),
                            "direccion": fake.name(),
                            "ubicacionLatitud": fake.name(),
                            "ubicacionLongitud": fake.name(),
                            "nombre": fake.name()
                        }
                        }                       
                     )


def evento_mock():
    return Evento(fake.uuid4(), fake.name(), datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), 
                  fake.uuid4(), fake.uuid4(), fake.name())


@patch('test.mock_session', autospec=True)
def test_crear_evento(mock_session,requests_mock):
    my_evento_mock = evento_mock()

    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_evento_mock
    session.query.return_value = query

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    crearEvento = crear_evento(session, my_evento_mock, headers={"Authorization": "Bearer"})
    result = crearEvento.execute()
    assert result == "Evento registrado con éxito"

@patch('test.mock_session', autospec=True)
def test_crear_evento_missing_requiredfield(mock_session,requests_mock):
    my_evento_mock = evento_mock()
    my_evento_mock.id_socio=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_evento_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_evento(session, my_evento_mock,""),
        service.execute()
        
    assert exc_info.value.code == 404


