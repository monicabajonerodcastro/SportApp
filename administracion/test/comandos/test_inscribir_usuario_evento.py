import datetime
import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from src.modelos.evento import Evento
from test.mock_session import MockSession

from src.comandos.inscribir_usuario_evento import InscribirUsuarioEvento
from src.modelos.evento_usuario_u import EventoUsuarioU
from test.mock_session import MockSession
from src.errores.errores import MissingRequiredField

fake = Faker()
_TOKEN = fake.uuid4()
_ID_EVENTO = fake.uuid4()

@pytest.fixture
def mock_session():
    return MockSession()


def crear_usuario_evento(session, evento_mock, headers):
    return InscribirUsuarioEvento(session,headers, evento_mock.id_evento )

def evento_usuario_mockq():
    return EventoUsuarioU(id_usuario=fake.uuid4(), id_evento=_ID_EVENTO)


@patch('test.mock_session', autospec=True)
def test_crear_evento(mock_session,requests_mock):
    my_evento_mock = evento_usuario_mockq()

    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_evento_mock
    session.query.return_value = query

    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN, "id_usuario": fake.uuid4()})
    crearEvento = crear_usuario_evento(session, my_evento_mock, headers={"Authorization": "Bearer"})
    result = crearEvento.execute()
    assert result == "Inscripción registrada con éxito"

@patch('test.mock_session', autospec=True)
def test_crear_evento_missing_requiredfield(mock_session,requests_mock):
    my_evento_mock = evento_usuario_mockq()
    my_evento_mock.id_evento=""
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_evento_mock
    session.query.return_value = query
    requests_mock.post('http://host-personas-test/personas/validar-token', json={"token": _TOKEN})
    
    with pytest.raises(MissingRequiredField) as exc_info:
        service = crear_usuario_evento(session, my_evento_mock,""),
        service.execute()
        
    assert exc_info.value.code == 404


