import datetime
import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from src.comandos.actualizar_evento import ActualizarEvento
from test.mock_session import MockSession


from src.modelos.evento import Evento
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField

fake = Faker()
_TOKEN = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


def actualizar_evento(session, evento_mock, headers):
    return ActualizarEvento(session,headers,
                        {"id": evento_mock.id,
                        "fecha_inicio": evento_mock.fecha_inicio,
                        "fecha_fin": evento_mock.fecha_fin,
                                               
                        }                       
                     )


def evento_mock():
    return Evento(fake.uuid4(), fake.name(), datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), datetime.datetime.strptime(fake.date(),'%Y-%m-%d'), 
                  fake.uuid4(), fake.uuid4(), fake.name())


@patch('test.mock_session', autospec=True)
def test_actualizar_evento(mock_session,requests_mock):
    my_evento_mock = evento_mock()

    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_evento_mock
    session.query.return_value = query

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    actualizarEvento = actualizar_evento(session, my_evento_mock, headers={"Authorization": "Bearer"})
    result = actualizarEvento.execute()
    assert result == "Evento actualizado con exito"

@patch('test.mock_session', autospec=True)
def test_actualizar_evento_missing_requiredfield(mock_session,requests_mock):
    my_evento_mock = evento_mock()
    my_evento_mock.id_socio=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_evento_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    with pytest.raises(MissingRequiredField) as exc_info:
        service = actualizar_evento(session, my_evento_mock,""),
        service.execute()
        
    assert exc_info.value.code == 404


